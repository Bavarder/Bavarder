{
  description = "Bavarder";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }: let
    systems = ["aarch64-linux" "x86_64-linux"];
  in
    flake-utils.lib.eachSystem systems (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        bavarder = pkgs.python3Packages.buildPythonApplication rec {
          pname = "bavarder";
          version = self.rev or "dirty";
          pyproject = false;

          src = ./.;

          patches = [
            # Removes gpt4all support. It would be lots of work to package it properly
            # and we already have ollama with working ROCm + CUDA in nixpkgs.
            ./0001-remove-gpt4all-support.patch
          ];

          nativeBuildInputs = with pkgs; [
            appstream-glib
            blueprint-compiler
            desktop-file-utils
            gettext
            gtk4
            meson
            ninja
            pkg-config
            wrapGAppsHook4
          ];

          buildInputs =  with pkgs; [
            gtksourceview5
            libadwaita
            libportal
          ];

          propagatedBuildInputs = with pkgs.python3Packages; [
            babel
            gst-python
            lxml
            openai
            pygobject3
            requests
          ];

        };
      in {
        formatter = pkgs.alejandra;

        checks.bavarder = bavarder;
        packages.default = bavarder;

        devShells.default = pkgs.mkShell.override {stdenv = pkgs.python3Packages.stdenv;} {
          inherit (bavarder) nativeBuildInputs buildInputs propagatedBuildInputs;
        };
      }
    );
}