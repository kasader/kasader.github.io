{
  description = "Hugo (Go) development environment.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.hugo
            # Hugo Modules are Go modules; `hugo mod` shells out to both.
            pkgs.go
            pkgs.git
            # Hugo dropped libsass, so extended-only SCSS themes need the
            # dart-sass transpiler on PATH.
            pkgs.dart-sass
            pkgs.gopls
            pkgs.golangci-lint

            # Extra tooling for lint/styling
            pkgs.markdownlint-cli2
            pkgs.typos
            pkgs.lychee
          ];

          shellHook = ''
            echo "hugo dev shell ready"
          '';
        };
      }
    );
}
