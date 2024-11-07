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
        in
        with pkgs;
        {
          devShells.default = mkShell {
            buildInputs = [
              pkgs.gnumake
              pkgs.stdenv.cc.cc.lib
              pkgs.gcc
              pkgs.libstdcxx5
              pyright
              pkgs.direnv
              pkgs.ruff
              pkgs.poetry
            ];
            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc
                pkgs.libstdcxx5
              ]}
            '';
          };
        }
      );
}
