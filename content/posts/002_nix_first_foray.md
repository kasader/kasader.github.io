---
title: "Declarative Systems With Nix"
date: 2026-05-12
tags: ["nix", "linux"]
---

A local development environment is usually a set-and-forget affair (until something breaks, anyway). Mine had accreted for years across two machines and two operating systems, and the state of each was known only to whichever shell history survived last. So I rebuilt the whole thing declaratively with **Nix**, and I have been enjoying the process far more than I expected to.

My daily drivers are a ThinkPad X1 Carbon Gen 6 running **NixOS**, and a work MacBook Pro running **nix-darwin**. Maintaining a single source of truth across Linux and macOS sounds like it ought to be miserable. It isn't. Installation on the ThinkPad was the barebones CLI installer with no desktop environment, and because Nix does the actual work of resolving and building everything, I had my full toolchain running inside of two hours.

All of my configuration lives on GitHub, split across [`nix-declarative`](https://github.com/kasader/nix-declarative) for the flake, modules and hosts, and [`home-manager`](https://github.com/kasader/home-manager) for the earlier standalone setup. The usual caveat applies: I am very much still a Nix novice, and you should not take anything in either repository as best practice just yet.

Much of the appeal of Nix is that it declines to tell you how to structure your system. There is an enormous amount of latitude in how you write your declarations, and the ergonomics of the result are entirely yours to decide. In my flake I define `kasada@ramiel` for the ThinkPad and `kasada@israfel` for the Mac, and route both to the same terminal configuration, the same Neovim plugin set, and the same CLI tooling. No divergence/duplication/random exceptions like `if [[ "$(uname)" == "Darwin" ]]` scattered through a shell profile.

What makes that tractable is not the flake so much as the emergant shape that comes with making flakes usable beyond a single host. Rather than writing one configuration per machine, I write classes of capability and compose them, in three layers: modules declare what exists, profiles group them into classes, and hosts name only their own deviations.

---

## Layer 1: Modules Declare Capabilities

Everything installable is a home-manager module under `modules/`, grouped by what it *is* rather than by which machine wants it:

```text
modules
├── browsers
│   ├── default.nix
│   ├── firefox/default.nix
│   └── librewolf/default.nix
├── cloud/default.nix
├── containers/default.nix
├── default.nix
├── editors
│   ├── default.nix
│   └── nvim
│       ├── config/          # init.lua, lua/core, lua/plugins, lazy-lock.json
│       └── default.nix
├── files
│   ├── default.nix
│   └── yazi.nix
├── fonts/default.nix
├── fun/default.nix
├── k8s/default.nix
├── languages
│   ├── default.nix
│   ├── go.nix
│   ├── python3.nix
│   └── rust.nix
├── media/default.nix
├── security/default.nix
├── services
│   ├── default.nix
│   └── syncthing.nix
├── shell
│   ├── bash/default.nix
│   ├── default.nix
│   ├── fish/{abbrs,aliases,default,functions}.nix
│   ├── fzf/default.nix
│   ├── starship/default.nix
│   └── zsh/default.nix
├── terminal
│   ├── default.nix
│   ├── ghostty.nix
│   └── tmux.nix
└── vcs
    ├── default.nix
    ├── ghq.nix
    └── git.nix
```

Each leaf declares a `custom.<path>.enable` option and gates its entire `config` block behind it. The Kubernetes module is representative, and about as simple as they get:

```nix
{ config, lib, pkgs, ... }:
let
  cfg = config.custom.k8s;
in
{
  options.custom.k8s.enable = lib.mkEnableOption "Kubernetes tooling";

  config = lib.mkIf cfg.enable {
    home.packages = with pkgs; [
      kubectl kubernetes-helm kustomize k9s kubectx
      stern minikube kubeconform kube-linter conftest
    ];

    programs.fish.shellAbbrs = {
      k = "kubectl";
      kctx = "kubectx";
      kns = "kubens";
    };
  };
}
```

A module owns more than a package list. It owns the shell abbreviations, the environment variables, the config files, and anything else belonging to that capability. Turning `custom.k8s.enable` on gets me `kubectl` *and* my `k` abbreviation; turning it off takes both away. There is no half-configured state where the tool is present but the ergonomics around it are missing.

### Importing a Module Does Not Enable It

`modules/default.nix` imports every category, but an import only *declares* the option. Everything defaults to off:

```nix
imports = [
  ./editors ./languages ./terminal ./shell ./fonts ./vcs
  ./k8s ./containers ./browsers ./cloud ./security
  ./media ./fun ./files ./services
];
```

So "is this capability available?" and "is this capability on?" are answered in different files. Every host evaluates the full registry and chooses from it, which means adding a new module never changes an existing machine. That property is what makes the repository safe to extend on a whim.

### Adding Extra Options

A module is free to expose more than a toggle. The Go module takes a second option with a sensible default:

```nix
options.custom.languages.go = {
  enable = lib.mkEnableOption "Go ambient env (GOPATH/GOBIN) + optional global toolchain";
  installToolchain = lib.mkOption {
    type = lib.types.bool;
    default = true;
    description = "Install a global Go toolchain as a fallback for use outside project dev-shells.";
  };
};
```

Anything that enables Go inherits the global toolchain. A machine that would rather get its compiler exclusively from project dev-shells sets `installToolchain = false` and keeps the `GOPATH`/`GOBIN` ambient config regardless. The default serves the common case; the override stays one line, at whichever layer needs it.

Granularity is a per-category decision too. Browsers are individually toggleable, because I genuinely want different browsers on different machines. The shell stack is the opposite fish, zsh and starship are co-installed rather than alternatives, so they share a single `custom.shell.enable` and each child gates its own config on it. `fzf` sits in the same directory but kept its own toggle, since it is a distinct thing I might not want. The directory tree suggests a hierarchy; the options need not follow it slavishly.

---

## Layer 2: Profiles Compose Classes

Between the modules and the machines sit profiles, which are the classes I actually compose from. `profiles/home/base.nix` is the interactive core (what I want on anything I have a `home/` dir on), headless boxes included:

```nix
custom = {
  editors.nvim.enable = true;
  files.yazi.enable = true;
  shell = {
    enable = true;
    fzf.enable = true;
  };
  terminal.tmux.enable = true;
  vcs = {
    git.enable = true;
    ghq.enable = true;
  };
};
```

`profiles/home/workstation.nix` layers on everything that presumes a real personal machine, like a graphical session, dev toolchains, cloud accounts, media, toys:

```nix
custom = {
  fonts.enable = true;
  fun.enable = true;
  media.enable = true;
  security.enable = true;
  services.syncthing.enable = true;
  terminal.ghostty.enable = true;
  cloud = {
    aws.enable = true;
    gcp.enable = true;
    oci.enable = true;
  };
  languages = {
    go.enable = true;
    rust.enable = true;
    python3.enable = true;
  };
};
```

`profiles/home/darwin.nix` is the exception though. It just holds macOS glue rather than adding some capability (which is a concession that I kind of hate, but it's the only way to resolve on a non-pure Nix system). Because only Darwin hosts import it, nothing inside needs an `isDarwin` guard and therefore Linux never evaluates it. This also keeps Darwin-only packages, like per `orbstack`, off Linux entirely. Platform branching handled by composition instead of conditionals.

---

## Layer 3: Hosts Declare Only Deviations

The payoff is that a host file is nearly empty. Here is the Mac in full:

```nix
{ ... }: {
  imports = [
    ../../profiles/home/base.nix
    ../../profiles/home/workstation.nix
    ../../profiles/home/darwin.nix
  ];

  home = {
    username = "kasada";
    homeDirectory = "/Users/kasada";
  };

  # Per-host extras (the base profile already provides the universal set).
  custom = {
    browsers.firefox.enable = true;
    k8s.enable = true;
    containers.enable = true;
  };
}
```

The ThinkPad is the same file minus the Darwin profile and minus the container work, and my headless box imports `base.nix` and nothing else:

| Host      | Role                | Profiles                   | Host-local extras            |
| --------- | ------------------- | -------------------------- | ---------------------------- |
| `israfel` | work MacBook Pro    | base, workstation, darwin  | firefox, k8s, containers     |
| `ramiel`  | ThinkPad, NixOS     | base, workstation          | firefox                      |
| `nixbox`  | headless NixOS      | base                       | —                            |

Populating a new machine is therefore a matter of writing five lines of host file and choosing which classes apply. Everything downstream (dotfiles, shell abbreviations, Neovim plugin set, LSP servers, environment variables) arrives assembled. Nothing to remember; perfect for me brain! \*smiles\*

---

## Resources Worth Bookmarking

The reason any of this is tractable for a newcomer is the tooling the community has built (*something, something, we stand on the shoulders of giants, something, something*). Nix's language and module system are not especially forgiving, but the searchable references removed most of the guesswork for me:

- **[NixOS Packages](https://search.nixos.org/packages)** — the official package registry, and the first place to check.
- **[Home Manager Options](https://home-manager-options.extranix.com/)** — indispensable for finding the exact option path for user-level tooling.
- **[MyNixOS](https://mynixos.com/)** — good for browsing options and reading how other people have arranged their configurations.
- **[Nix.dev](https://nix.dev/)** — the official tutorials, and readable ones at that.

### Takeaway

Reproducing an entire OS and development environment from a single Git repository was worth the cost for me, but the reproducibility is only half of it. I did not anticipate what falls out of separating a capability's *definition* from its *activation*: modules describe what a thing is, profiles describe classes of machine, and hosts describe only their own deviations. I think that is the beauty of Nix that those incessent Nix guys on forums always rant and rave about (I suppose I am one now, too). Adding a tool touches one file; standing up a new machine touches one file; it's so nice. I am still working out how best to factor all of this out, and I still expect to rewrite plenty of it. But declaring what I want and letting the package manager work out how to get there is the right division of labour, and it is difficult to go back to anything else.
