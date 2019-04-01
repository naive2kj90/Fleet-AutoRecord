# README 한 번 읽어보기

import datetime as dt
import numpy as np
import glob, os, time, math, shutil, sys
from PIL import Image, ImageGrab, ImageEnhance, ImageOps, ImageFilter  # pip3 install pillow
import pyautogui as pag  # pip3 install pyautogui==0.9.39
from pytesseract import image_to_string # pip3 install pytesseract
import cv2  # pip3 install opencv-python
from mss import mss  # pip3 install mss

# initila settings
file_path = os.path.abspath(os.path.dirname(__file__))

correction1 = 85  # 스샷 위치에 따른 강적 딜 보정
correction2 = 85  # 스샷 위치에 따른 함대원 리스트 보정

f = open("n_participant.txt", "r")
n_participant = int(f.readline())  # 오늘 강척 친 인원
f.close()
f2 = open("n_fleet.txt", "r")
n_fleet = int(f2.readline())  # 현재 함대원 수
f2.close()

date_n = str(dt.datetime.now()).split(' ')[0].split('-')
date_n = date_n[0] + date_n[1] + date_n[2]

(width, height) = pag.size()


def image_crop():
	print("\nAttacker nick/dmg extract process...\n")
	img_list = glob.glob(file_path + "/images_source/s_atk/*.png")
	template = cv2.imread(file_path + '/images_source/bar.png', 0)
	# crop_area = (530, 220, 1060, 650)  # 4명 전체

	if not os.path.isdir(file_path + "/images_bk/bk_nick"):		
		os.mkdir(file_path + "/images_bk/bk_nick")
	if not os.path.isdir(file_path + "/images_bk/bk_dmg"):
		os.mkdir(file_path + "/images_bk/bk_dmg")

	for (idx, i) in enumerate(img_list):
		# print("i : ", i)
		# r,g,b,a = Image.open(i).split()
		# r,g,b = Image.open(i).split()
		# img2 = Image.merge('RGB', (r,g,b))
		img2 = Image.open(i)

		check = 4
		if idx == n_participant // 4:  # 남은 인원수에 대한 처리
			check = n_participant % 4

		for j in range(check):
			crop_area4 = (535, 220+(j+4-check)*116+correction1, 1060, 320+(j+4-check)*116+correction1)  # dmg 1
			cropped_img2 = img2.crop(crop_area4)
			cropped_img2.save('t_test' + str(j+1) + '.png')
			pos = imagesearch('t_test' + str(j+1) + '.png', template)
			# print("position : ", pos[0], pos[1])
			crop_area2 = (0, pos[1]+1, 1060-535, pos[1] + 41)
			cropped_img5 = cropped_img2.crop(crop_area2)
			cropped_img5.save(file_path + "/images_crop/" + str(idx*4+j).zfill(2) + ".png")

			crop_area_nick = (0, 0, 200, 40)  # nick 1
			crop_area_dmg = (375, 0, 525, 40)  # dmg 1

			crop_nick = bg_black(cropped_img5.crop(crop_area_nick))
			# crop_nick = ImageEnhance.Sharpness(crop_nick).enhance(3.0) # 닉 참 못 읽는다 ㅠㅠ
			# crop_nick = crop_nick.filter(ImageFilter.FIND_EDGES)
			crop_nick.save(file_path + "/images_bk/bk_nick/" + str(idx*4+j).zfill(2) + ".png")
			crop_dmg = bg_black(cropped_img5.crop(crop_area_dmg))
			# crop_dmg = crop_dmg.filter(ImageFilter.FIND_EDGES)
			crop_dmg.save(file_path + "/images_bk/bk_dmg/" + str(idx*4+j).zfill(2) + ".png")
			# txt_read(cropped_img2, cropped_img3)
			os.remove('t_test' + str(j+1) + '.png')


def fleet_crop():
	print("\nFleet crop process...\n")
	if not os.path.isdir(file_path + "/images_bk/bk_fleet"):
		os.mkdir(file_path + "/images_bk/bk_fleet")
	img_list2 = glob.glob(file_path + "/images_source/s_fleet/*.png")
	template2 = cv2.imread(file_path + '/images_source/bar2.png', 0)
	# crop_area_ = (250, 170, 520, 790)  # 4명 전체
	for (idx, i) in enumerate(img_list2):
		# print("i : ", i)
		img_2 = Image.open(i)
		#r,g,b,a = img_2.split()
		#img_2 = Image.merge('RGB', (r,g,b))
		check2 = 4
		if idx == n_fleet // 4:
			check2 = n_fleet % 4
		for j in range(check2):  # 4 5
			crop_area_4 = (250, 170+(j+4-check2)*162+correction2, 520, 343+(j+4-check2)*162+correction2)
			cropped_img_2 = img_2.crop(crop_area_4)
			cropped_img_2.save('t_test' + str(j+1) + '.png')
			pos = imagesearch('t_test' + str(j+1) + '.png', template2)
			crop_area_2 = (39, pos[1]-60, 249, pos[1]-10)
			crop_nick_fleet = bg_black(cropped_img_2.crop(crop_area_2))
			# crop_nick_fleet = crop_nick_fleet.filter(ImageFilter.FIND_EDGES)  # 테두리
			crop_nick_fleet.save(file_path + "/images_bk/bk_fleet/" + str(idx*4+j).zfill(2) + ".png")
			os.remove('t_test' + str(j+1) + '.png')


def imagesearch(image_1, template, precision=0.8, method=None):
	# https://steemit.com/python/@howo/image-recognition-for-automation-with-python
	img_gray = cv2.imread(image_1, 0)
	if method == None:
		method = cv2.TM_CCOEFF_NORMED
	else:
		method = cv2.TM_CCOEFF
	res = cv2.matchTemplate(img_gray, template, method)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	if max_val < precision:
		return [-1,-1]
	return max_loc


def bg_black(image_1, thres=255):
	ww, hh = image_1.size
	rgb_img = image_1.load()
	bw_image = Image.new("RGB", (ww, hh), (0, 0, 0))
	bw = bw_image.load()
	for i in range(ww):
		for j in range(hh):
			if not rgb_img[i, j] == (thres, thres, thres):
				bw[i, j] = (0, 0, 0)
			else:
				# bw[i, j] = (rgb_img[i, j])
				bw[i, j] = (255, 255, 255)
	# bw_image = ImageOps.invert(bw_image)#.convert('LA')  # 반전 & 흑백처리
	return bw_image


def img_merge():
	print('\nimg merge process')
	new_image = Image.new("RGB", (210, n_fleet * 50), (0, 0, 0))
	fleet_list = glob.glob(file_path + "/images_bk/bk_fleet/*.png")
	for (idx, j) in enumerate(fleet_list):
		area = (0, idx*50, 210, (idx+1)*50)
		new_image.paste(Image.open(j), area)
	# new_image.show()
	new_image.save(file_path + "/images_bk/f_list.png")


def hit_compare():
	print("\nHit comparing\n")
	compare_result = [-1 for _ in range(n_participant)]
	result = [-1 for _ in range(n_fleet)]
	# print("c : ", compare_result)
	hit_list = glob.glob(file_path + "/images_bk/bk_nick/*.png")
	fleet_list = glob.glob(file_path + "/images_bk/bk_fleet/*.png")
	f_list = cv2.imread(file_path + '/images_bk/f_list.png', 0)
	# for (idx, j) in enumerate(fleet_list):
	for (idx, i) in enumerate(hit_list):
		pos = imagesearch(i, f_list, 0.75, 1)
		if not pos[0] == -1:
			# print("Hit idx : ", idx)
			compare_result[idx] = pos[1] // 50
			result[compare_result[idx]] = 1  # dmg로 나중에 수정
		else:
			print("\n----- 함대원 리스트 재촬영 요망 -----\n")
			#sys.exit(1)

	print("\nidx_result : ", compare_result)
	#'''
	ccc = 0
	for ii in range(n_participant):
		for jj in range(n_participant):
			if compare_result[ii] == compare_result[jj]:
				ccc = ccc + 1
		ccc = ccc - 1
	print("\nError : ", ccc/(n_participant), " : ← 0 이 아니면 문제 있음!")
	#'''

	if not os.path.isdir(file_path + "/images_result"):
		os.mkdir(file_path + "/images_result")
	if not os.path.isdir(file_path + "/images_result/" + date_n):
		os.mkdir(file_path + "/images_result/" + date_n)

	f = open(file_path + "/images_result/" + date_n + '/' + date_n + '_result.txt', 'w')
	for i in range(n_fleet):
		f.write(str(result[i]))
		if not i == n_fleet - 1:
			f.write('\n')
	f.close()

	return compare_result


def result_img(c_result):
	print('\nresult image making process...\n')

	result_image = Image.new("RGB", (680, n_participant * 40), (0, 0, 0))
	result_yes = Image.new("RGB", (210, n_participant * 50), (0, 0, 0))
	result_no = Image.new("RGB", (210, (n_fleet - n_participant) * 50), (0, 0, 0))
	template1 = cv2.imread(file_path + '/images_source/bar.png', 0)
	template2 = cv2.imread(file_path + '/images_source/bar2.png', 0)

	s_list = glob.glob(file_path + "/images_source/s_atk/*.png")
	f_list = glob.glob(file_path + "/images_source/s_fleet/*.png")

	for (idx, i) in enumerate(s_list):  # 데미지 결과
		img2 = Image.open(i)
		# r,g,b,a = Image.open(i).split()
		# r,g,b = Image.open(i).split()
		# img2 = Image.merge('RGB', (r,g,b))
		check = 4
		if idx == n_participant // 4:  # 남은 인원수에 대한 처리
			check = n_participant % 4
		for j in range(check):
			crop_area4 = (0, 220+(j+4-check)*116+correction1, 1060, 320+(j+4-check)*116+correction1)  # dmg 1
			cropped_img2 = img2.crop(crop_area4)
			cropped_img2.save('t_test' + str(j+1) + '.png')
			pos = imagesearch('t_test' + str(j+1) + '.png', template1)
			crop_area2 = (380, pos[1]+1, 1060, pos[1] + 41)
			cropped_img5 = cropped_img2.crop(crop_area2)

			area2 = (0, (idx*4+j)*40, 680, (idx*4+j+1)*40)
			result_image.paste(cropped_img5, area2)
			os.remove('t_test' + str(j+1) + '.png')

	check_y, check_n = 0, 0
	for (idx, i) in enumerate(f_list):	# 참여/미참여 그룹 구분
		#r,g,b,a = Image.open(i).split()
		#img_2 = Image.merge('RGB', (r,g,b))
		img_2 = Image.open(i)
		check2 = 4
		if idx == n_fleet // 4:  # 남은 인원수에 대한 처리
			check2 = n_fleet % 4
		for j in range(check2):
			crop_area_4 = (250, 170+(j+4-check2)*162+correction2, 520, 343+(j+4-check2)*162+correction2)
			cropped_img_2 = img_2.crop(crop_area_4)
			cropped_img_2.save('t_test' + str(j+1) + '.png')
			pos = imagesearch('t_test' + str(j+1) + '.png', template2)
			crop_area_2 = (39, pos[1]-60, 249, pos[1]-10)
			crop_nick_fleet = cropped_img_2.crop(crop_area_2)

			if (idx*4+j) in c_result:
				area3 = (0, check_y*50, 210, (check_y+1)*50)
				result_yes.paste(crop_nick_fleet, area3)
				check_y = check_y + 1
				# print("yy : ", check_y)
			else:
				area3 = (0, check_n*50, 210, (check_n+1)*50)
				result_no.paste(crop_nick_fleet, area3)
				check_n = check_n + 1			
				# print("nn : ", check_n)
			os.remove('t_test' + str(j+1) + '.png')

	result_image.save(file_path + "/images_result/" + date_n + '/' + date_n + "_강적결과.png")
	result_yes.save(file_path + "/images_result/" + date_n + '/' + date_n + "_강적O.png")
	result_no.save(file_path + "/images_result/" + date_n + '/' + date_n + "_강적X.png")

	print('\nresult image making done\n')


def screenshot1():
	img_dir1 = file_path + "/images_source/s_atk"
	if not os.path.isdir(img_dir1):
		os.mkdir(img_dir1)
	date_n = str(dt.datetime.now()).split(' ')[1].split('.')[0].split(':')
	date_n = date_n[0] + date_n[1] + date_n[2]

	with mss() as sct:
		sct.shot(output=img_dir1 + "/" + date_n + ".png")


def screenshot2():
	img_dir1 = file_path + "/images_source/s_fleet"
	if not os.path.isdir(img_dir1):
		os.mkdir(img_dir1)
	date_n = str(dt.datetime.now()).split(' ')[1].split('.')[0].split(':')
	date_n = date_n[0] + date_n[1] + date_n[2]

	with mss() as sct:
		sct.shot(output=img_dir1 + "/" + date_n + ".png")


def s_clear():
	img_dir1 = file_path + "/images_source/s_atk"
	if os.path.isdir(img_dir2):
		shutil.rmtree(img_dir2)
	os.mkdir(img_dir2)
	img_dir2 = file_path + "/images_source/s_fleet"
	if os.path.isdir(img_dir2):
		shutil.rmtree(img_dir2)
	os.mkdir(img_dir2)


def txt_read(nick, dmg):  # 미구현.
	# http://m.blog.daum.net/geoscience/1266
	# https://github.com/UB-Mannheim/tesseract/wiki
	s_w = image_to_string(nick, lang='kor').split('\n')[0]
	s_w2 = image_to_string(dmg, lang='eng').split('\n')[0]
	print("nick / dmg : ", s_w, " / ", s_w2, ".")


#if __name__ == '__main__':
def main():
	print("\n---- Start ----")

	img_dir = file_path + "/images_crop"

	if not os.path.isdir(img_dir):
		os.mkdir(img_dir)

	if not os.path.isdir(file_path + "/images_bk"):
		os.mkdir(file_path + "/images_bk")
	else:
		shutil.rmtree(file_path + "/images_bk")
		os.mkdir(file_path + "/images_bk")

	# mousemove2(n_participant)  # 마우스 움직여서 매크로 촬영. 오토핫키를 통해 구현.
	image_crop()  # 강적 친 사람들 닉네임/DMG 추출
	fleet_crop()  # 현재 함대원 명단 추출
	img_merge()  # 현재 함대원 명단 이미지 1개로 합치기
	c_result = hit_compare()  # 강적 누가 쳤나 구분
	result_img(c_result)  # 보여주기용 output 이미지 생성

	shutil.rmtree(img_dir)  # 임시 경로 삭제

	print("\n---- END ----")
