# Kolor Scope (W.I.P)

A color name detection and classification tool implemented in Python. It features both a live (through the webcam using OpenCV) and static image-based color picker with real-time feedback based on Euclidean distance in RGB space between the selected color and name entries in a dataset, as well as a color name classifier that assigns simple color name labels to color hex codes based on HSL similarity.

All contributions are welcome, feel free to fork, comment suggestions, tips or add pull requests.

> [!NOTE]  
> This project is a work in progress.

# Features

Through this project you are able to select a/series of pixel(s) through different methods of image inputs and view the hex code, exotic color name and simple color name of the selected pixel(s).
This benefits individuals with colorblindness or those wanting to learn about uncommon color names.

**This app supports two methods for image inputs, selectable via the "Source" tab:**
1. **Image Mode**, which Loads an image with .jpg, .jpeg, .png, .bmp and .gif (a static frame for now) formats.
2. **Camera Mode**, which renders the webcam feed of the device.

**This app also supports two methods for selecting pixels from the source image via the "Selection Mode" tab:**
1. **Pixel mode**, which a single pixel can be selected and its color is shown as an output.
2. **Area mode**, in which the user can select a series of pixel in a rectangular shaped area and the most prominent color of that area is shown as the output.

<div align="center">

![Pixel](https://github.com/user-attachments/assets/5b314fd2-c922-4b05-9521-ef1462bdffb4)

**Pixel Selection Mode Being Tested on the Image Mode**

![Area](https://github.com/user-attachments/assets/7103b087-bb09-40fd-9321-ed43f76f27c6)

**Area Selection Mode Being Tested on the Image Mode**

![Camera](https://github.com/user-attachments/assets/7f0bebdc-5ed4-4b92-b128-39636fb6af16)

**Pixel Selection Mode Being Tested on the Live Camera Mode**

</div>


# Compile, Build and Run

**Prerequisites :**
* Install the following Python packages:  
`pip install pillow numpy opencv-python pyinstaller`

**Make sure project resources are present in the root folder :**

1. Make sure **base_colors.csv** is in the root folder. (check **# References** for credits)
2. Make sure **cleaned_colors.csv** is in the root folder.
* If the **cleaned_colors.csv** dataset is missing, or you wish to make changes to it and the color names that reside inside it you must do it by executing the **simple_color_name_filler.py** script.
* Run the following command in project root:<br>
`python simple_color_name_filler.py`
3. Make sure **icon.ico** is present in project root.

**If all resources are present, execute the kolor_scope.py script :**
* Run the following command in project root:<br>
`python kolor_scope.py`
 
**To create an exe build of the project :**
1. Make sure all the previously mentioned resources are available in the project root as well as **kolor_scope.py**, then run the following:<br>
`pyinstaller --onefile --windowed --icon=icon.ico --add-data "cleaned_colors.csv;." kolor_scope.py`
2. Your **kolor_scope.exe** should be available in the newly created **dist** folder, copy and paste both **icon.ico** and **cleaned_colors.csv** into the dist folder alongside the exe.
3. Run your program :). Also make sure **icon.ico** and **cleaned_colors.csv** are always coupled with the exe. 


## ⚠️ Known Issues

* In Area selection mode black and white pixels might be disproportionately weighing and influencing the most prominent color.
* Accuracy in assigning simple color labels (`simple_color_name_filler.py`) is off and might cause some mismatch.

# References
The base "color-names" dataset is pulled from the following GitHub repository.   
By David Aerne (meodai)  
[_meodai GitHub Repository_](https://github.com/meodai/color-names)
