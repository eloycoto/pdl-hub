{
  description = "Langchain flake with tools";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    eloy.url = "github:eloycoto/nix-custom-overlay";
  };
  outputs = { self, nixpkgs, flake-utils, eloy }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [eloy.overlays.default];
          };
          python-packages = ps: with ps; [
            flake8
            # pyyaml
            # pydantic
            # litellm
            termcolor
            build
            ipython
            ipdb
            flask
            html2text
          ];
        in
        with pkgs;
        {
          devShells.default = mkShell {
            buildInputs = [
              (pkgs.python3.withPackages python-packages)
              pkgs.gnumake
              pyright
              pkgs.direnv
              pkgs.ruff
              pkgs.python3Packages.prompt-declaration-language
            ];

          };
        }
      );
}
