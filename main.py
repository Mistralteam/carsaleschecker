from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
import json

BASE_URL = 'https://www.carsales.com.au'
BASE_URL_TEMPLATE = f'{BASE_URL}/cars/{{make}}/{{model}}/{{badge}}-badge/{{state}}-state/?page='
YEAR_RANGE_URL_TEMPLATE = f'{BASE_URL}/cars/?q=(And.(C.Make.{{make}}._.(C.Model.{{model}}._.Badge.{{badge}}.))_.State.{{state}}._.Year.range({{min_year}}..{{max_year}}).)'
NUM_PAGES = 1  # Default value for number of pages to scrape



def manual_selection():
    global driver
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    messagebox.showinfo("Info",
                        "Please select make, model, badge, etc., manually on the browser and then come back to the GUI and hit 'Scrape Now'. Do not close the browser.")


def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def start_scraping():
    global NUM_PAGES
    if 'driver' not in globals() or not driver.service.process:
        messagebox.showerror("Error", "Please select the car details manually in the browser first.")
        return

    NUM_PAGES = int(pages_spinbox.get())

    for page_num in range(1, NUM_PAGES + 1):
        if page_num != 1:
            driver.get(driver.current_url.split('?')[0] + '?page=' + str(page_num))
            time.sleep(5)
            try:
                page_source = driver.page_source
            except Exception as e:
                print(f"Error occurred: {e}")
                return

            soup = BeautifulSoup(page_source, 'html.parser')
    car_listings = soup.find_all('div', class_='listing-item')
    car_data = []

    for listing in car_listings:
        car_info = {}
        car_info['NetworkID'] = listing.get('data-webm-networkid')
        car_info['Category'] = listing.get('data-webm-vehcategory')
        car_info['BodyStyle'] = listing.get('data-webm-bodystyle')
        car_info['Make'] = listing.get('data-webm-make')
        car_info['Model'] = listing.get('data-webm-model')
        car_info['State'] = listing.get('data-webm-state')
        car_info['Price'] = listing.get('data-webm-price')
        badge_tag = listing.find('span', class_='csn-badge-title')
        car_info['Badge'] = badge_tag.text.strip() if badge_tag else None
        car_name_tag = listing.find("a", class_="js-encode-search")
        if car_name_tag:
            car_info['Name'] = car_name_tag.text.strip()
            car_info['Link'] = car_name_tag['href']
        images = []
        for img in listing.select(".carousel-item img"):
            img_src = img.get('src') or img.get('data-src')
            if img_src:
                images.append(img_src)
        car_info['Images'] = images
        key_details = {}
        for li in listing.select(".key-details li"):
            label = li.get('data-type')
            if label:
                key_details[label] = li.text.strip()
        car_info['KeyDetails'] = key_details
        car_data.append(car_info)

    if price_filter_var.get() == 1:
        car_data = [car for car in car_data if car.get('Badge') in ['Well below market price', 'Below market price']]

    if car_data:
        save_to_csv(car_data, 'cars_data.csv')
        messagebox.showinfo("Success", "Data has been saved to cars_data.csv")
    else:
        messagebox.showerror("Error", "No data found. Please check your selections and try again.")

app = tk.Tk()
app.title("Car Data")

price_filter_var = tk.IntVar()
price_filter_checkbox = tk.Checkbutton(app, text="Well under market price", variable=price_filter_var)
price_filter_checkbox.pack(pady=10)

# Add a label and Spinbox for page selection
pages_label = tk.Label(app, text="Number of Pages to Scrape:")
pages_label.pack(pady=10)

pages_spinbox = tk.Spinbox(app, from_=1, to=100)  # assuming max pages is 100
pages_spinbox.pack(pady=10)

manual_selection_button = tk.Button(app, text="Manual Selection", command=manual_selection)
manual_selection_button.pack(pady=20)

scrape_button = tk.Button(app, text="Scrape Now", command=start_scraping)
scrape_button.pack(pady=20)

app.mainloop()