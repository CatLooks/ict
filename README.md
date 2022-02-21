# ICT (Image Compiling Tool)
This small program is designed to create images from layout files written in XML.

# Usage
Program accepts one argument: layout file path:
<code>py ict.py [file]</code>

# Syntax
Each layout file has a common syntax. The following code contains all features available in ICT.
```xml

<?xml version="1.0" encoding="utf-8"?>
<root>
  <!--
    The following variable types are used here:
    * V = variable name (any string)
    * F = file name (file path)
    * N = number
    * B = boolean (true / false)
    * C = color (#RGB / #RGBA / #RRGGBB / #RRGGBBAA)
    * T = text (any text)
    * S = system font name
  -->
  
  <!-- header of the output image -->
  <header size="NxN" file="F" ? resize="NxN" fg="C" bg="C"/>
  
  <!-- used resources -->
  <resources>
    <!-- import image (or a part of image) -->
    <image name="V" file="F" ? position="N,N" size="NxN"/>
    <!-- import text from file -->
    <text name="V" file="F"/>
    <!-- import font from file -->
    <font name="V" file="F" size="N" ? bold="B" italic="B"/>
    <!-- import font from system -->
    <font name="V" id="S" size="N" ? bold="B" italic="B"/>
  </resources>
  
  <!-- image layout -->
  <layout>
    <!-- blit image -->
    <tag type="image" name="V" ? position="N,N" size="NxN"/>
    <!-- blit text from file -->
    <tag type="label" source="V" ? position="N,N" center="B,B" antialias="B" fg="C" bg="C"/>
    <!-- blit raw text -->
    <tag type="label" text="T" ? position="N,N" center="B,B" antialias="B" fg="C" bg="C"/>
    <!-- blit plane -->
    <tag type="plane" fill="C" ? position="N,N" size="N,N"/>
  </layout>
</root>

```
