import xmltodict as xml
import pygame as py
import sys

hex_nums = '0123456789ABCDEF'

def error(*args):
	sys.stderr.write(' '.join(args) + '\n')

def mul(coords, scale):
	return [coords[0] * scale[0], coords[1] * scale[1]]

def convert(text):
	text = text.strip()

	if text.lower() == 'true':
		return True
	if text.lower() == 'false':
		return False
	if text.lower() == 'null':
		return None

	def ti(s):
		s = s.strip()
		if s.lower() == 'true':
			return True
		if s.lower() == 'false':
			return False
		if s.lower() == 'null':
			return None
		if s.endswith('h'):
			return int(s[:-1], 16)
		if s.endswith('b'):
			return int(s[:-1], 2)
		if s.endswith('px'):
			return int(s[:-2])
		if s.endswith('cm'):
			return int(float(s[:-2]) * 96)
		if s.endswith('mm'):
			return int(float(s[:-2]) * 96 // 10)
		if s.endswith('dm'):
			return int(float(s[:-2]) * 960)
		return int(float(s))

	if text.startswith('#'):
		if len(text) == 4:
			return [hex_nums.index(text[1].upper()) * 17,
					hex_nums.index(text[2].upper()) * 17,
					hex_nums.index(text[3].upper()) * 17,
					255]
		if len(text) == 5:
			return [hex_nums.index(text[1].upper()) * 17,
					hex_nums.index(text[2].upper()) * 17,
					hex_nums.index(text[3].upper()) * 17,
					hex_nums.index(text[4].upper()) * 17]
		if len(text) == 7:
			return [hex_nums.index(text[1].upper()) * 16 + hex_nums.index(text[2].upper()),
					hex_nums.index(text[3].upper()) * 16 + hex_nums.index(text[4].upper()),
					hex_nums.index(text[5].upper()) * 16 + hex_nums.index(text[6].upper()),
					255]
		if len(text) == 9:
			return [hex_nums.index(text[1].upper()) * 16 + hex_nums.index(text[2].upper()),
					hex_nums.index(text[3].upper()) * 16 + hex_nums.index(text[4].upper()),
					hex_nums.index(text[5].upper()) * 16 + hex_nums.index(text[6].upper()),
					hex_nums.index(text[7].upper()) * 16 + hex_nums.index(text[8].upper())]
		raise ValueError('invalid color')

	if 'x' in text:
		return list(map(ti, text.split('x')))
	if ',' in text:
		return list(map(ti, text.split(',')))

	return ti(text)

def evaluate(layout):
	# create surface
	dst = py.Surface(convert(layout['header'][0]['@size']))

	# default values
	FGC = layout['header'][0].get('@fg', '#000000FF')
	BGC = layout['header'][0].get('@bg', 'null')
	SCALE = convert(layout['header'][0].get('@scale', '1,1'))

	# load resources
	imgs = {}
	txts = {}
	fnts = {}
	if 'resources' in layout:
		if 'image' in layout['resources'][0]:
			for img in layout['resources'][0]['image']:
				imgs[img['@name']] = (
					py.image.load(img['@file']),
					convert(img.get('@position', '0,0')),
					convert(img.get('@size', 'null'))
				)

		if 'text' in layout['resources'][0]:
			for txt in layout['resources'][0]['text']:
				with open(txt['@file']) as f:
					txts[txt['@name']] = f.read()

		if 'font' in layout['resources'][0]:
			for fnt in layout['resources'][0]['font']:
				if '@file' in fnt:
					fnts[fnt['@name']] = py.font.Font(fnt['@file'], convert(fnt.get('@size', '12')),
						convert(fnt.get('@bold', 'false')), convert(fnt.get('@italic', 'false')))
				else:
					fnts[fnt['@name']] = py.font.SysFont(fnt['@id'], convert(fnt.get('@size', '12')),
						convert(fnt.get('@bold', 'false')), convert(fnt.get('@italic', 'false')))

	# create image
	for tag in layout['layout'][0]['tag']:
		if tag['@type'] == 'image':
			img = imgs[tag['@name']]

			src = img[0]
			if '@size' in tag:
				src = py.transform.scale(img[0], mul(convert(tag['@size']), SCALE))

			if img[2]:
				dst.blit(src, mul(convert(tag.get('@position', '0,0')), SCALE), (img[1], img[2]))
			else:
				dst.blit(src, mul(convert(tag.get('@position', '0,0')), SCALE))

		elif tag['@type'] == 'label':
			fnt = fnts[tag['@font']]

			if '@source' in tag:
				txt = txts[tag['@source']]
			else:
				txt = tag['@text']

			img = fnt.render(txt, convert(tag.get('@antialias', 'true')), convert(tag.get('@fg', FGC)), convert(tag.get('@bg', BGC)))
			f = convert(tag.get('@position', '0,0'))
			x, y = mul(f, SCALE)
			u, v = convert(tag.get('@center', 'false,false'))
			if u:
				x -= img.get_width() // 2
			if v:
				y -= img.get_height() // 2

			dst.blit(img, (x, y))

		elif tag['@type'] == 'plane':
			if ('@position' not in tag) and ('@size' not in tag):
				dst.fill(convert(tag.get('@fill', '#00000000')))
			else:
				py.draw.rect(dst, convert(tag.get('@fill', '#00000000')),
					(mul(convert(tag.get('@position', '0,0')), SCALE), mul(convert(tag.get('@size', '0,0'))), SCALE))

	# save surface
	if '@resize' in layout['header'][0]:
		dst = py.transform.scale(dst, convert(layout['header'][0]['@resize']))
	py.image.save(dst, layout['header'][0]['@file'])

def compile(path):
	with open(path) as f:
		try:
			layout = xml.parse(f.read(), force_list=True)
		except Exception as exc:
			error('[PARSE ERROR]:', str(exc))
			return
		
		try:
			evaluate(layout['root'][0])
		except KeyError as exc:
			error('[KEY ERROR]:', str(exc))
		except ValueError as exc:
			error('[VALUE ERROR]:', str(exc))
		except FileNotFoundError as exc:
			error('[FILE ERROR]:', str(exc))

if __name__ == '__main__':
	if len(sys.argv) == 1:
		raise SystemExit

	py.init()
	compile(sys.argv[1])