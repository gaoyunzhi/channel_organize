#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import time
import plain_db
import webgram
import post_2_album
from bs4 import BeautifulSoup
import cached_url
import os
import export_to_telegraph

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

def getPosts(channel):
	start = time.time()
	result = []
	posts = webgram.getPosts(channel)[1:]
	for post in posts:
		yield post
	while posts:
		pivot = posts[0].post_id
		posts = webgram.getPosts(channel, posts[0].post_id, 
			direction='before', force_cache=True)[1:]
		for post in posts:
			yield post

def getAlbums(posts):
	for post in posts:
		try:
			yield post_2_album.get('https://t.me/' + post.getKey()), post
		except Exception as e:
			print('post_2_album failed', post.getKey(), str(e))

def getLinkReplace(url, album):
	if 'telegra.ph' in url and 'douban.com/note/' in album.cap_html:
		return ''
	if 'douban.com/' in url:
		return '\n\n' + url
	if 'telegra.ph' in url:
		soup = BeautifulSoup(cached_url.get(url, force_cache=True), 'html.parser')
		title = export_to_telegraph.getTitle(url)
		try:
			return title + ' ' + soup.find('address').find('a')['href']
		except:
			return ''
	return url

def getText(album, post):
	soup = BeautifulSoup(album.cap_html, 'html.parser')
	for item in soup.find_all('a'):
		if item.get('href'):
			item.replace_with(getLinkReplace(item.get('href'), album))
	for item in soup.find_all('br'):
		item.replace_with('\n')
	text = soup.text.strip()
	if post.file:
		text += '\n\n' + album.url
	return text

def getVideoTitle(album, post):
	title = album.cap_html
	for separator in '\n <':
		if len(title.split(separator)[0]) > 6:
			title = title.split(separator)[0]
	if title.find('】') != -1:
		title = title.split('】')[0] + '】'
	return title

def run():
	for channel in credential['channels']:
		for album, post in getAlbums(getPosts(channel)):
			if album.video:
				print(getVideoTitle(album, post), album.url)
			
if __name__ == '__main__':
	run()