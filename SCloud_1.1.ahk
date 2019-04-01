^g::

	ww = 1920
	hh = 1080
	FileRead, n_fleet, n_fleet.txt
	c := n_fleet//4
	c1 := c//3
	c2 := c - c1*2
	dh3 = 693  ; 함대원 체크시 마우스 움직이는 거리
	dh4 := dh3+2
	ahk_dir := A_ScriptDir
	py_dir := ahk_dir "\" "python.exe"

	;MouseClick, 버튼, X, Y, 클릭 횟수, 속도, 버튼 누르고 있기|떼기, 상대 좌표
	MouseMove, ww/2-550, hh/2+300, 30,
	MouseClick, left, 0, 0, , , , R	; 함대원 명단 클릭
	sleep, 2000
	MouseMove, ww/2-250, hh/2+250, 30,	; 드래그 할 위치로 이동
	sleep, 500

	MouseClick, left, 0, 0, , 30 ,D , R	; D는 누르고 있기 설정
	MouseMove, 0, -15, 30, R  ; 초기 위치 조절
	sleep, 1000
	MouseClick, left, 0, 0, , 30, U, R
	MouseMove, 0, 15, 30, R

	Run, python.exe
	sleep, 1500
	WinMove, %py_dir%, , 500, 850
	sleep, 200

	send import fleet_ar
	send {Enter}
	sleep, 500

	send fleet.s_clear()
	send {Enter}
	sleep, 1000

	Loop, %c1%
	{	
		send fleet_ar.screenshot2()
		send {Enter}
		sleep, 2000
		MouseClick, left, 0, 0, , , , R
		sleep, 500
		MouseClick, left, 0, 0, , 60 ,D , R	;D는 누르고 있기 설정
		MouseMove, 0, -%dh3%, 30, R
		sleep, 1000
		MouseClick, left, 0, 0, , 60, U, R
		MouseMove, 0, %dh3%, 30, R
		sleep, 500
		WinActivate, %py_dir%
		sleep, 500
	}
	Loop, %c1%
	{
		send fleet_ar.screenshot2()
		send {Enter}
		sleep, 2000
		MouseClick, left, 0, 0, , , , R
		sleep, 500
		MouseClick, left, 0, 0, , 60 ,D , R	;D는 누르고 있기 설정
		MouseMove, 0, -%dh4%, 30, R
		sleep, 1000
		MouseClick, left, 0, 0, , 60, U, R
		MouseMove, 0, %dh4%, 30, R
		sleep, 500
		WinActivate, %py_dir%
		sleep, 500
	}
	Loop, %c2%
	{
		send fleet_ar.screenshot2()
		send {Enter}
		sleep, 2000
		MouseClick, left, 0, 0, , , , R
		sleep, 500
		MouseClick, left, 0, 0, , 60 ,D , R	;D는 누르고 있기 설정
		MouseMove, 0, -%dh3%, 30, R
		sleep, 1000
		MouseClick, left, 0, 0, , 60, U, R
		MouseMove, 0, %dh3%, 30, R
		sleep, 500
		WinActivate, %py_dir%
		sleep, 500
	}
	send fleet_ar.screenshot2()
	send {Enter}
	sleep, 2000

	IfWinExist, %py_dir%
	WinClose

	sleep, 500	; 함대원 읽는 과정 종료


	FileRead, n_participant, n_participant.txt
	b := n_participant//4
	b1 := b//3
	b2 := b - b1
	dh = 485  ; 강적 딜 체크시 마우스 움직이는 거리
	dh2 := dh+7

	; 함대 명단에서 시작
	MouseMove, ww/2-770, hh/2-400, 10,
	MouseClick, left, 0, 0, , , , R	; 뒤로가기 클릭
	sleep, 1500
	MouseMove, ww/2+700, hh/2-150, 10,	;
	MouseClick, left, 0, 0, , , , R	; BOSS공략 클릭
	sleep, 1500
	MouseMove, ww/2-850, hh/2+235, 10,	;
	MouseClick, left, 0, 0, , , , R	; 랭킹확인 클릭
	sleep, 1500

	;MouseClick, 버튼, X, Y, 클릭 횟수, 속도, 버튼 누르고 있기|떼기, 상대 좌표
	MouseMove, ww/2 + 250, hh/2 + 180, 30,	; 드래그 할 위치로 이동
	MouseClick, left, 0, 0, , , , R

	sleep, 500
	MouseClick, left, 0, 0, , 30 ,D , R	; D는 누르고 있기 설정
	MouseMove, 0, -30, 30, R  ; 초기 위치 조절
	sleep, 1000
	MouseClick, left, 0, 0, , 30, U, R
	MouseMove, 0, 30, 30, R

	Run, python.exe
	sleep, 1500
	WinMove, %py_dir%, , 500, 850
	sleep, 200

	send import fleet_ar
	send {Enter}
	sleep, 500

	Loop, %b1%
	{
		send fleet_ar.screenshot1()
		send {Enter}
		sleep, 2000
		MouseClick, left, 0, 0, , , , R
		sleep, 500
		MouseClick, left, 0, 0, , 60 ,D , R	;D는 누르고 있기 설정
		MouseMove, 0, -%dh%, 30, R
		sleep, 1000
		MouseClick, left, 0, 0, , 60, U, R
		MouseMove, 0, %dh%, 30, R
		sleep, 500
		WinActivate, %py_dir%
		sleep, 500
	}
	Loop, %b2%
	{
		send fleet_ar.screenshot1()
		send {Enter}
		sleep, 2000
		MouseClick, left, 0, 0, , , , R
		sleep, 500
		MouseClick, left, 0, 0, , 60 ,D , R	;D는 누르고 있기 설정
		MouseMove, 0, -%dh2%, 30, R
		sleep, 1000
		MouseClick, left, 0, 0, , 60, U, R
		MouseMove, 0, %dh2%, 30, R
		sleep, 500
		WinActivate, %py_dir%
		sleep, 500
	}

	send fleet_ar.screenshot1()
	send {Enter}
	sleep, 2000

	;send import fleet_ar.main()
	;send {Enter}

	;sleep, 10000  ; 10초
	IfWinExist, %py_dir%  ; cmd창 종료
	WinClose


	Run, python.exe
	sleep, 1500

	send import fleet_ar
	send {Enter}
	sleep, 500

	send fleet_ar.main()
	send {Enter}
	sleep, 10000

	msgbox, , ,모든 과정 종료!, 10

Return


^h::
	Exitapp
return