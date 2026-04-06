{
  description = "Bavarder";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    let
      systems = [
        "aarch64-linux"
        "x86_64-linux"
      ];
    in
    flake-utils.lib.eachSystem systems (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        litert-lm-api-nightly = pkgs.python3Packages.buildPythonApplication rec {
          pname = "litert-lm-api-nightly";
          version = "0.10.0.dev20260405";
          format = "wheel";

          src = pkgs.fetchurl {
            url = "https://files.pythonhosted.org/packages/31/6a/9942b0216289ec631a6b842dd6973b57eb58a3194516d509c306f74a1ba5/litert_lm_api_nightly-${version}-cp313-cp313-manylinux_2_35_x86_64.whl";
            hash = "sha256-gkrP5Y3/CLNCr5lzXLlEdHQeG2LPRP9VGv2Sku41TAc=";
          };

          dependencies = with pkgs.python3Packages; [
            numpy
          ];
        };

        litert-lm-nightly = pkgs.python3Packages.buildPythonApplication rec {
          pname = "litert-lm-nightly";
          version = "0.10.0.dev20260405";
          format = "wheel";

          src = pkgs.fetchurl {
            url = "https://files.pythonhosted.org/packages/d6/d8/269de6dc0a8715e9b6665349f9d5d8beb9c76977f844339736e13a47c387/litert_lm_nightly-${version}-py3-none-any.whl";
            hash = "sha256-mQYmzdaRScLDLhJ+xaTG7DrdAd7BvMakY2fccWXQOiw=";
          };

          dependencies = with pkgs.python3Packages; [
            litert-lm-api-nightly
            click
            huggingface-hub
            prompt-toolkit
          ];
        };

        bavarder = pkgs.python3Packages.buildPythonApplication rec {
          pname = "bavarder";
          version = self.rev or "dirty";
          pyproject = false;

          src = ./.;

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

          buildInputs = with pkgs; [
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
            pillow
            requests
            litert-lm-api-nightly
            litert-lm-nightly
          ];

        };
      in
      {
        formatter = pkgs.alejandra;

        checks.bavarder = bavarder;
        packages.default = bavarder;

        devShells.default = pkgs.mkShell.override { stdenv = pkgs.python3Packages.stdenv; } {
          inherit (bavarder) nativeBuildInputs buildInputs propagatedBuildInputs;
        };
      }
    );
}
