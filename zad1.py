#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280

def read_bme280():
    """Read environmental data from the BME280 sensor."""
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    
    bme280.sea_level_pressure = 1013.25
    return {
        "temperature": bme280.temperature,
        "humidity": bme280.humidity,
        "pressure": bme280.pressure,
        "altitude": bme280.altitude
    }

def draw_environmental_data(draw, font_large, font_small, data):
    """Draw sensor data on the OLED display with icons."""
    draw.rectangle([(0, 0), (96, 64)], outline="BLACK", fill="BLACK")
    
    # Draw temperature icon and value
    draw.text((5, 5), "ἲ1", font=font_large, fill="WHITE")  # Thermometer icon
    draw.text((25, 5), f"{data['temperature']:.1f} °C", font=font_small, fill="WHITE")
    
    # Draw humidity icon and value
    draw.text((5, 25), "☔", font=font_large, fill="WHITE")  # Umbrella icon
    draw.text((25, 25), f"{data['humidity']:.1f} %", font=font_small, fill="WHITE")
    
    # Draw pressure icon and value
    draw.text((5, 45), "⛈", font=font_large, fill="WHITE")  # Cloud with lightning icon
    draw.text((25, 45), f"{data['pressure']:.1f} hPa", font=font_small, fill="WHITE")

def oled_display():
    """Initialize OLED display and show environmental data."""
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()
    
    # Load fonts
    font_large = ImageFont.truetype('./lib/oled/Font.ttf', 18)
    font_small = ImageFont.truetype('./lib/oled/Font.ttf', 14)
    
    while True:
        # Read sensor data
        data = read_bme280()
        
        # Create a new image for drawing
        image = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image)
        
        # Draw environmental data with icons
        draw_environmental_data(draw, font_large, font_small, data)
        
        # Display the image on the OLED
        disp.ShowImage(image, 0, 0)
        
        # Wait before updating again
        time.sleep(2)

def test():
    print("\nRunning BME280 and OLED display test...")
    oled_display()

if __name__ == "__main__":
    test()

