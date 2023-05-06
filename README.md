
<h1 align="center">
  <img src="data/icons/hicolor/scalable/apps/io.github.Bavarder.Bavarder.svg" alt="Bavarder" width="192" height="192"/>
  <br>
  Bavarder
</h1>

<p align="center">
  <strong>Chit-chat with an AI</strong>
</p>

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
</p>

<p align="center">
  <a href="https://stopthemingmy.app">
    <img alt="Please do not theme this app" src="https://stopthemingmy.app/badge.svg"/>
  </a>
</p>

<p align="center">
  <img src="./data/screenshots/quantum-computing.png" alt="Preview"/>
</p>

## About the name

Bavarder is a french word, the definiton of Bavarder is "Parler abondamment de choses sans grande portée" (Talking a lot about things that don't matter) (Larousse) which can be translated by Chit-Chat (informal conversation about matters that are not important). For non-french speakers, Bavarder can be hard to speak, it's prounouced as [bavaʀde]. Hear [here](https://youtu.be/9Qoogwxo5YA)

## Installation

### Flatpak

#### Flathub

You can either use your GNOME Software and search for "Bavarder" or you can run

``` shell
flatpak install io.github.Bavarder.Bavarder
```

#### Latest build

You can download the latest Flatpak build from [Github Actions](https://github.com/Bavarder/Bavarder/actions/workflows/build.yml). Click on the latest job and download the artifact.

#### From Source

Clone the repo and run `flatpak-builder`

``` shell
git clone https://codeberg.org/Bavarder/Bavarder # or https://github.com/Bavarder/Bavarder
cd Bavarder
flatpak-builder --install --user --force-clean repo/ build-aux/flatpak/io.github.Bavarder.Bavarder.json
```

## Contribute

The [GNOME Code of Conduct](https://wiki.gnome.org/Foundation/CodeOfConduct) is applicable to this project

See [`SEEN.md`](./SEEN.md) for a list of articles and posts about Bavarder

### Translate

<a href="https://translate.codeberg.org/engage/bavarder/">
<img src="https://translate.codeberg.org/widgets/bavarder/-/multi-auto.svg" alt="Translation status" />
</a>

You can translate Bavarder using Codeberg Translate

### Mirrors

- [Github](https://github.com/Bavarder/Bavarder)
- [Codeberg](https://codeberg.org/Bavarder/Bavarder)

## See also 

### Imaginer : Imagine with AI 

A tool for generating pictures with AI (GNOME app)

- https://github.com/ImaginerApp/Imaginer
- https://codeberg.org/Imaginer/Imaginer
