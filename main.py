# coding: utf8

import argparse
import sys
from google_images_download import google_images_download
from colorthief import ColorThief

def downloadImages(search, sample_size):
    response = google_images_download.googleimagesdownload()
    arguments = { "keywords": search,
                  "limit": sample_size,
                  "print_urls":False}
    paths = response.download(arguments)
    return(paths)

def getAverageRGB(paths, quality):
    rgb_values = []
    for path in paths:
        try:
            color_thief = ColorThief(path)
            # get the dominant color
            dominant_color = color_thief.get_color(quality=quality)
            # build a color palette
            #print(dominant_color)
            rgb_values.append(dominant_color)
        except Exception as e:
            continue
    average_rgb = tuple([num // len(rgb_values) for num in list(map(sum, zip(*rgb_values)))])
    return average_rgb

def estimateColour(search,
                   sample_size=5,
                   quality=5):
    paths = downloadImages(search,sample_size)[0][search]
    average_rgb = getAverageRGB(paths,quality)
    return(average_rgb)

def main():
    parser = argparse.ArgumentParser(
            description='Google Image Colour Estimator')

    parser.add_argument(
            'search',
            metavar='search',
            type=str,
            help='A string containing the search terms'
    )
    args = parser.parse_args()

    print(estimateColour(args.search))

main()
