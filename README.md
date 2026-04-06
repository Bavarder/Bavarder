<a href="https://bavarder.codeberg.page">
<h1 align="center">
  <img src="data/icons/hicolor/scalable/apps/io.github.Bavarder.Bavarder.svg" alt="Bavarder" width="192" height="192"/>
  <br>
  Bavarder
</h1>

<p align="center">
  <strong>Chit-chat with an AI</strong>
</p>
</a>

<p align="center">
  <a href="https://flathub.org/apps/details/io.github.Bavarder.Bavarder">
    <img width="200" alt="Download on Flathub" src="https://dl.flathub.org/assets/badges/flathub-badge-i-en.svg"/>
  </a>
  <br>
</p>

<br>

<p align="center">
   <a href="https://translate.codeberg.org/engage/bavarder/">
    <img src="https://translate.codeberg.org/widgets/bavarder/-/svg-badge.svg" alt="Translation status" />
  </a>
  <a href="https://repology.org/project/bavarder/versions">
    <img alt="Packaging status" src="https://repology.org/badge/tiny-repos/bavarder.svg">
  </a>
  <a href="https://snapcraft.io/bavarder">
    <img alt="bavarder" src="https://snapcraft.io/bavarder/badge.svg" />
  </a>
</p>

<a href="https://bavarder.codeberg.page">
<p align="center">
  <img src="./data/screenshots/preview.png" alt="Preview"/>
</p>
</a>

## Usage

Documentation is available [here](https://bavarder.codeberg.page)

## Installation

### Nix

Nix is used to develop Bavarder, there is also a Nix flake available at [flake.nix](./flake.nix). You can run Bavarder without installing it by running

``` shell
nix run github:Bavarder/Bavarder
```

### Flatpak

You can either use your GNOME Software and search for "Bavarder" or you can run

``` shell
flatpak install io.github.Bavarder.Bavarder
```

### Latest

You can download a flatpak from the latest commit [here](https://codeberg.org/Bavarder/-/packages/generic/bavarder/). Run

``` shell
curl -s -o bavarder.flatpak https://codeberg.org/api/packages/Bavarder/generic/Bavarder/164/bavarder.flatpak && flatpak install --user bavarder.flatpak -y 
```

#### From Source

### Nix

Just clone the repo and run `nix develop` and you will be in a shell with all the dependencies installed, you can then run `nix run` to run the app or `nix build` to build it

``` shell
git clone https://github.com/Bavarder/Bavarder # or https://codeberg.org/Bavarder/Bavarder
cd Bavarder
nix develop
nix run # Run the app
nix build # Build the app
```

### Flatpak-builder

Clone the repo and run `flatpak-builder`

``` shell
git clone https://codeberg.org/Bavarder/Bavarder # or https://github.com/Bavarder/Bavarder
cd Bavarder
flatpak-builder --install --user --force-clean repo/ build-aux/flatpak/io.github.Bavarder.Bavarder.json
```
### Meson

``` shell 
git clone https://codeberg.org/Bavarder/Bavarder # or https://github.com/Bavarder/Bavarder
cd Bavarder
meson setup build # Configure the build environment in subdirectory 'build'
meson compile -C build
meson check -C build
meson install -C build
chmod 0755 /usr/local/bin/bavarder # Fix binary permissions
```

### Others

You can see more install methods on the [website](https://bavarder.codeberg.page/install/)

## Contribute

The [GNOME Code of Conduct](https://wiki.gnome.org/Foundation/CodeOfConduct) is applicable to this project

### Translate

<a href="https://translate.codeberg.org/engage/bavarder/">
    <img src="https://translate.codeberg.org/widgets/bavarder/-/multi-auto.svg" alt="Translation status" />
</a>

You can translate Bavarder using [Codeberg Translate](https://translate.codeberg.org/engage/bavarder/)

## Mirrors

- [GitHub](https://github.com/Bavarder/Bavarder)
- [GitLab](https://gitlab.com/Bavarder/Bavarder)
- [Codeberg](https://codeberg.org/Bavarder/Bavarder)

## About the name

Bavarder is a french word, the definiton of Bavarder is "Parler abondamment de choses sans grande portée" (Talking a lot about things that don't matter) (Larousse) which can be translated by Chit-Chat (informal conversation about matters that are not important). For non-french speakers, Bavarder can be hard to speak, it's prounouced as [bavaʀde]. Hear [here](https://youtu.be/9Qoogwxo5YA)
