# Switch 2 (and switch 1) NDS Emulator

## Origins
This project is based on [switch-gba](https://github.com/itsbjoern/switch-gba), it uses Desmume instead of mGBA.

It's a working progress NDS emulator for the Nintendo Switch 2 (and any Nintendo Switch 1 model even lite or OLED).

<details>
  <summary>Information / How it's done</summary>
  This project makes use of the Switch browser that comes up when trying to verify / sign in with certain DNS providers. Please take a look at [Switchbru](https://www.switchbru.com/dns/).

  The way the Switch handles `B` is a bit different if there is an iFrame present on the page. In this case `B` will actually navigate the iFrame back first **before** navigating back the actual page (or reloading it). This is crucial for my workaround. With the use of `postMessage` I always immediately return to a "navigated" state of the iFrame.
</details>

---
## Planned features
* [Done]  NDS Games support
* Audio support
* Touchscreen support
* X and Y buttons support
* Add a button to mimic the Microphone 
* Eventually switch to a fork of desmume that supports Wifi Connections

---
## Usage

**Windows 10/11**
To host this emulator on Windows 10 or 11, you just need to download the latest release, extract the .zip and launch the switch-nds.exe

Keeps in mind that you can add your `.nds` roms in the `roms` folder, by default this folder is empty.

**Linux**
Assuming you installed Python 3.10 before (Python 3.14 will not works).

Clone this repo with the following command :
```bash
git clone https://github.com/Gabriel-Chevallier/switch-nds.git
```

Go in the clone repo folder :
```bash
cd switch-nds
```

And you just need to runs the run.sh script :
```bash
chmod u+x run.sh
./run.sh
```
## Versions

## 1.0.0
* Initial release

## Resources

Switch supported HTML features http://html5test.com/s/a77ccd45f1540617.html
