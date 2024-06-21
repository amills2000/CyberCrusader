<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/amills2000/CyberCrusader">
    <img src="images/logo.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">CyberCrusader</h3>

  <p align="center">
    Incident Response Triage Analyser Framework
    <br />
    <br />
    <a href="https://github.com/amills2000/CyberCrusader/CyberCrusader/issues">Report Bug</a>
    ·
    <a href="https://github.com/amills2000/CyberCrusader/CyberCrusader/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The idea behind this project is to simplify the analysis of triage artifacts gathered during and incidents, specially if you have a high number of machines to analyze. The idea is to scale this project by adding new modules that can parse new artifacts from different sources. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This project is based on python 3.0 and you will need to have it install on the machine to run it.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/amills2000/CyberCrusader.git
   ```
2. Install python requirements
   ```
   pip install -r requirements.tx
   ```
3. Copy the backup config file
    ```
    cp ./configs.json.back ./configs.json
    ```
4. Add the 7zip binary to /Modules/tools/7zip/7z.exe

#### Optional 

The INSTALL.bat can be used to add the run button to the context menu.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run the script use the following command: 

```
python ./main.py -p "path-to-your-triages"
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/amills2000/CyberCrusader.svg?style=for-the-badge
[contributors-url]: https://github.com/amills2000/CyberCrusader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/amills2000/CyberCrusader.svg?style=for-the-badge
[forks-url]: https://github.com/amills2000/CyberCrusader/network/members
[stars-shield]: https://img.shields.io/github/stars/amills2000/CyberCrusader.svg?style=for-the-badge
[stars-url]: https://github.com/amills2000/CyberCrusader/stargazers
[issues-shield]: https://img.shields.io/github/issues/amills2000/CyberCrusader.svg?style=for-the-badge
[issues-url]: https://github.com/amills2000/CyberCrusader/issues
[license-shield]: https://img.shields.io/github/license/amills2000/CyberCrusader.svg?style=for-the-badge
[license-url]: https://github.com/amills2000/CyberCrusader/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/marc-amills
[Python]: https://img.shields.io/badge/Python-35495E?style=for-the-badge&logo=python&logoColor=FFFF00
[python-url]: https://www.python.org/
