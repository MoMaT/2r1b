#!/usr/bin/env python

import os
import json
import textwrap
import subprocess
import lxml.etree as ET

from copy import deepcopy


class Cards:
	"""
	Changes dicionary keys to object fields.

	"""
	def __init__(self, data):
		if type(data["color"]) is not list:
			data["color"] = [data["color"]]
		self.__dict__.update(data)


def multiline(lines, height, element, offset=0):
	"""
	Show text in separate lines.

	"""
	x = element.get("x")
	y = element.get("y")

	span = element.getchildren()[0]
	span.set("x", x)
	span.set("y", str(int(y) + offset))
	span.text = lines[0]

	position = int(y) + height + offset
	for line in lines[1:]:
		span = ET.SubElement(element, "tspan", x=x, y=str(position))
		span.text = line
		position += height


def add_text(element, card):
	"""
	Replaces the template card text with the name and description
	of the role.

	"""
	# modify description
	if element.get("font-size").startswith("12"):
		lines = []
		for line in card.text.split("\n"):
			if line:
				lines.extend(textwrap.wrap(line, 32))
			else:
				lines.append("")
		multiline(lines, 12, element)

	# modify character name
	elif element.get("font-size").startswith("36"):
		name = "Spy" if card.name.endswith("spy") else card.name
		if len(name) < 15:
			span = element.getchildren()[0]
			span.text = name
		else:
			element.set("font-size", "28")
			multiline(name.split(), 28, element, offset=-24)


# read roles
cards = {}
with open("data/cards.json") as config:
	data = json.load(config)
	for name, attributes in data.items():
		d = dict(name=name, color=attributes[0], text=attributes[1])
		cards[name] = Cards(d)

# setup pages
pages = []
pages.append([cards["Citizen"]] * 8)
pages.append([cards["Terrorist"]] * 8)
roles = "President, Bomber, Doctor, Engineer, Nurse, Tinkerer, President's daughter, Martyr"
pages.append([cards[name] for name in roles.split(", ")])
roles = "Hero, Dr. Boom, blue spy, red spy, Gambler, Detective, Survivor, Rival"
pages.append([cards[name] for name in roles.split(", ")])
roles = "Negotiator, Coy boy, Angel, Demon"
pages.append([cards[name] for name in roles.split(", ")])
roles = "Therapist, Paranoid, Mime, Paparazzi"
pages.append([cards[name] for name in roles.split(", ")])

# read template files data
svg = {}
for color in ["blue", "red", "grey"]:
	tree = ET.parse("data/{0}.svg".format(color))
	svg[color] = tree.getroot().getchildren()

# generate pages
nsmap = {None: "http://www.w3.org/2000/svg"}
for n, page in enumerate(pages):
	document = ET.Element("svg", width="100%", height="100%", version="1.1", viewBox="0 0 1052 744", nsmap=nsmap)
	main_group = ET.SubElement(document, "g", transform="translate(107, 45)", nsmap=nsmap)

	# place cards in the centre of a page in a 4x2 grid
	i = 0
	for card in page:
		# cards may have more than one color
		for color in card.color:
			x = i * 210 if i < 4 else (i - 4) * 210
			y = 0 if i < 4 else 327
			i += 1

			card_group = ET.SubElement(main_group, "g", transform="translate({0}, {1})".format(x, y), nsmap=nsmap)
			template = svg[color]

			# for spy role, add different color header
			if card.name.endswith("spy"):
				for element in template[:5]:
					card_group.append(deepcopy(element))
				template = svg[card.name.split()[0]][5:]

			# add SVG elements from the template card
			for element in template:
				element = deepcopy(element)
				if element.tag.endswith("text"):
					add_text(element, card)
				card_group.append(element)

	# save constructed SVG image as file
	with ET.xmlfile("page.svg", encoding='utf-8') as xml:
		xml.write_declaration(standalone=False)
		xml.write(document)

	# convert SVG to PDF
	cmd = "inkscape --export-pdf=page-{0}.pdf page.svg".format(n + 1)
	subprocess.call(cmd.split())

os.remove("page.svg")
