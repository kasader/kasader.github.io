---
title: "Zero-Allocation Logging in Go"
date: 2026-04-07
tags: ["go", "compilers"]
---

Go's structured logging library (`log/slog`), although maybe kind of boring at first glance, is a really quite clever piece of standard library code. That is: if you dive into how exactly they are able to process log attributes with **zero heap allocations**. Although the solution (which was inspired by the `uber-go/zap` and `rs/zerolog` packages), and this way of using the  `log/slog.Logger` is usually not that important for generic logging use-cases, it is extremely well-optimized for any hot-path application.

Thus, accordingly, I wanted to understand exactly how Go achieves this, as well as how the compiler optimizes away unnecessary overhead; so I wrote a quick mock logger implementation which is loosely based on `log/slog` and analyzed the output assembly via [compiler explorer (go.godbolt.org)](https://www.google.com/search?q=https://go.godbolt.org) (shoutout to [Matt Godbolt](https://xania.org/MattGodbolt), btw).

Below, I am going to walk through how the compiler avoids "boxing" ([allocating variables to the heap when converting to interfaces](https://goperf.dev/01-common-patterns/interface-boxing/)), completely inlines function calls to save CPU cycles, and passes data between stack frames without copying entire arrays.

## The Setup

Here is a stripped-down version of how a zero-allocation logger takes in attributes. Instead of using `...any` (which forces Go to box primitives into interfaces on the heap), we define a concrete `intAttr` struct.

```go
package p

import "fmt"

func myFunction(x int) int {
	log("my message", newIntAttr("k1", x), newIntAttr("k2", 2))
	return 0
}

//go:noinline
func log(msg string, attrs ...intAttr) {
	fmt.Print(msg)
	for _, attr := range attrs {
		fmt.Print(attr)
	}
}

type intAttr struct {
	key   string
	value int
}

func newIntAttr(k string, v int) intAttr {
	return intAttr{
		key:   k,
		value: v,
	}
}
```

When we compile this, we get a fat block of Plan 9 Assembly (I suggest you follow along using the same code above on the site if you want to fully understand the process). But before we decode the output, let's first address the weird symbol naming.

### The `command-line-arguments` Quirk

If you look at the raw assembly, you'll see memory locations and function calls prefixed with `command-line-arguments`, like this:

`CALL command-line-arguments.log(SB)` or `MOVQ DX, command-line-arguments..autotmp_8+40(SP)`.

Why? In Go's assembly dialect, the assembler attaches human-readable symbols to memory locations to help the debugger and the Garbage Collector map machine code back to your source file. When you compile a standalone Go file without a properly initialized Go module (like in a compiler explorer sandbox), the compiler assigns it a default package name of `command-line-arguments`.

The `..autotmp_8` simply means the compiler created a hidden, "automatic temporary" variable on the stack to hold our data. The CPU never sees these names; it only sees the raw memory offsets.

---

## Optimization 1: Function Inlining & Struct Initialization

In our Go code, we call `newIntAttr("k1", x)` and `newIntAttr("k2", 2)`. You might expect the assembly to set up a stack frame, push arguments, jump to the `newIntAttr` function, and return a struct.

The Go compiler is much smarter than that. It completely **inlines** the calls to save CPU cycles.

A Go `string` is a 16-byte struct (an 8-byte pointer to the text, and an 8-byte length). Our `int` is 8 bytes. That means each `intAttr` struct is exactly 24 bytes. Because we pass two of them in our variadic `...intAttr` slice, the compiler needs 48 bytes of contiguous memory.

Instead of calling `newIntAttr`, the compiler manually writes the data directly to the stack, byte by byte:

```asm
        // --- Building the first intAttr: newIntAttr("k1", x) ---
        // Grab the pointer to the "k1" string bytes and put it in DX
        LEAQ    go:string."k1"(SB), DX 
        // Write the Pointer to SP+40
        MOVQ    DX, command-line-arguments..autotmp_8+40(SP) 
        // Write the string Length (2) to SP+48
        MOVQ    $2, command-line-arguments..autotmp_8+48(SP) 
        // Write the integer value (x, held in AX) to SP+56
        MOVQ    AX, command-line-arguments..autotmp_8+56(SP) 

        // --- Building the second intAttr: newIntAttr("k2", 2) ---
        // Grab the pointer to the "k2" string bytes and put it in DX
        LEAQ    go:string."k2"(SB), DX
        // Write the Pointer to SP+64
        MOVQ    DX, command-line-arguments..autotmp_8+64(SP)
        // Write the string Length (2) to SP+72
        MOVQ    $2, command-line-arguments..autotmp_8+72(SP)
        // Write the integer value (2) to SP+80
        MOVQ    $2, command-line-arguments..autotmp_8+80(SP)
```

---

## Optimization 2: Escape Analysis and the Stack

Notice _where_ it wrote those 48 bytes: `+40(SP)` up through `+80(SP)`. `SP` is our **Stack Pointer**.

If we had passed our attributes as `...any` (the standard `fmt.Printf` approach), the compiler wouldn't know the size or type of the arguments at compile time. It would be forced to allocate them dynamically on the heap (a process called "boxing"), which requires the Garbage Collector to clean them up later.

Because we used a concrete type (`intAttr`), the compiler's **Escape Analysis** kicked in. It realized this variadic slice never "escapes" the lifecycle of `myFunction` and `log`. Therefore, it entirely skips the `runtime.newobject` heap allocation and safely builds the array directly within `myFunction`'s local stack space. This is the zero allocation we are looking for!

---

## Optimization 3: The Register-Based Calling Convention

Now that we have a 48-byte backing array on `myFunction`'s stack, how do we pass it to `log`? A common misconception is that the whole array is copied into the new function's stack frame.

Thanks to Go's modern register-based ABI (Application Binary Interface), arguments are passed to functions via CPU registers whenever possible. Our `log` function expects two arguments: a `string` (Pointer, Length) and a `slice` (Pointer, Length, Capacity).

Right before the `CALL` to `log`, the compiler packs these 5 words of data into 5 CPU registers:

| **Register** | **Argument**     | **Value**                  | **Assembly Instruction**                            |
| ------------ | ---------------- | -------------------------- | --------------------------------------------------- |
| `AX`         | `msg` Pointer    | Address of `"my message"`  | `LEAQ go:string."my message"(SB), AX`               |
| `BX`         | `msg` Length     | 10                         | `MOVL $10, BX`                                      |
| `CX`         | `attrs` Pointer  | Address of the Stack Array | `LEAQ command-line-arguments..autotmp_8+40(SP), CX` |
| `DI`         | `attrs` Length   | 2                          | `MOVL $2, DI`                                       |
| `SI`         | `attrs` Capacity | 2                          | `MOVQ DI, SI`                                       |

```asm
        CALL    command-line-arguments.log(SB)
```

When execution jumps into `log`, the 48 bytes of array data are left untouched, sitting safely back in `myFunction`'s stack frame. The `log` function simply uses the pointer passed in the `CX` register to reach "up" the stack and read the structs one by one.

### Takeaway

By passing a 24-byte slice header in registers rather than copying a whole 48-byte array across stack frames, and by avoiding the heap completely, Go keeps function calls blazingly fast. This combination of **inlining**, **stack allocation**, and **register-passing** is the exact same sauce that makes standard library packages like `log/slog` so performant.

...and... so now you know!
