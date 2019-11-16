# 2019-2 객체지향 프로그래밍 프로젝트 - **BOX HEAD - The Goblin**
구성원: 2-3 김진욱 | 2-6 박정민

## 1. 주제
학교로 들어오는 악령을 마법으로 막는다.
TPS

## 2. 동기
TPS 플래시 게임인 BOX HEAD 는 좀비가 적으로 나오는 게임이다. 이들을 공격하기 위해 플레이어는 다양한 총기/화기를 사용한다. 그러나 본인은 총기류에 익숙하지 않기에 Boxhead의 아이템으로 나오는 총기들의 특성을 이해하기 어려워 총기가 아닌 본인에게 조금 더 친숙한 판타지적 요소, 마법을 공격으로 사용하는 게임을 만들어보고 싶었다.  
수업을 듣거나 자습을 하다보면 ‘자고싶다’, ‘게임하고싶다’등의 유혹이 든다. 이러한 유혹이 사실 악령에 의한 것이 였다면 어떨까 생각하였다. 그러한 악령들로부터 우리 학생들을 수호하여 쾌적한 학습환경을 만들어주는 수호자가 존재하면 좋겠다는 생각에 그러한 설정을 가진 주인공을 만들어, 세종과학예술학교 건물을 배경으로 악령을 퇴치하는 게임을 만들게 되었다.

## 3. 프로그램 사용 대상
학교를 수호하고 있다는 사명감을 가지고 스트래스를 해소하고 싶어하는 SASA의 학생들

## 4. 목적
- 교칙을 어기지 않고 학생이 스트래스를 적절히 해소할 수 있는 5~10분 동안 플레이 할 수 있는 짧은 텀의 게임을 만든다.
- 중독성이 옅어 학업에 방해 되지 않는 선에서 스트래스를 해소할 수 있는 게임을 만든다.
- 총기가 아닌 마법류의 공격을 하는 만큼, 공격에 의한 디버프 효과에 집중한 게임을 만든다.

## 5. 주요기능
1. 스프라이트를 이용한 화려한 애니메이션
	- 스프라이트 이미지를 적극 활용하여, 캐릭터의 움직임이나, 스킬을 화려하게 만든다.
1. 악령  
	1. 종류  
		1. 검둥이
		    - hp : 매우 작음
		    - 공격력 : 매우 작음
		    - 이동속도 : 매우 빠름
		1. 초록이
		    - hp : 작음
		    - 공격력 : 보통
		    - 이동속도 : 보통
		1. 하양이
		    - hp : 보통 (+ hp 회복 능력)
		    - 공격력 : 매우 강함
		    - 이동속도 : 느림
		1. 파랑이(boss)
		    - hp : 매우 큼
		    - 공격력 : 보통
		    - 이동속도 : 느림
		    - 특수 능력 : 스킬이 관통하지 못함
1. 여러 종류의 마법 공격
    1. data
        1. 공격력
        1. 사출속도
        1. 상태이상능력
  	1. 종류
		1. fireball
		    - 화상상태 유발 : 매초 최대 체력의 5% 데미지
		1. blade
		    - 관통능력 없음. 순간 데미지가 강함.
		    - 마비 : 수초간 움직이지 않음. 공격도 하지 않음
		1. leaf
		    - 슬로우상태 유발 : 속도 75% 감소
		1. dark
		    - 혼란상태 유발 : 이동 방향 무작위
1. hp / mp 시스템  
	- hp는 체력으로, 악령과 접촉할시 악령에 공격력 만큼 매 초 마다 깎인다.  
	- mp는 스킬을 사용할 때 필요한 에너지로, 매초 일정량 회복된다. 최대치는 600이다.
2. 학교를 배경으로 한 스테이지  
	- hp 가 0이 될 때까지 진행된다.
	- 악령은 맵 양 옆 외각에서 스폰되며, 스폰 속도는 점점 빨라진다.

## 6. 프로젝트 핵심
- sprite 를 이용한 화려한 움직임과 스킬.  
- 학교를 배경으로한 SASA 학생을 위한 게임.

## 7. 구현에 필요한 라이브러리나 기술
pygame  
스프라이트 이미지를 이용한 애니메이션  

## 8. **분업 계획**
김진욱 : 마법 공격, 점수판 프로그래밍, 스프라이트 이미지 수집.  
박정민 : 스프라이트를 이용한 캐릭터 이동. 맵 제작. 몹스폰. 몹AI.

## 9. 기타

hitbox)
https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision/
https://nightshadow.tistory.com/entry/pygame-%EC%9D%98-%EC%8A%A4%ED%94%84%EB%9D%BC%EC%9D%B4%ED%8A%B8-%EC%B6%A9%EB%8F%8C%EC%B2%B4%ED%81%AC-%EB%B0%A9%EB%B2%95

마법)
https://opengameart.org/content/water-magic-effect
https://opengameart.org/content/cosmic-time-magic-effect
https://opengameart.org/content/pure-projectile-magic-effect 
https://www.seekpng.com/ipng/u2q8q8i1u2t4q8i1_animation-sprite-electric-blue-lightning-game-lightning-animation/ 
https://avangs.info/resource_200x/159728

캐릭터)
https://opengameart.org/content/fumiko-complete-charset
https://www.deviantart.com/my-invader-mia/art/Creepypasta-Sprite-sheet-505118676
https://github.com/skoam/fumiko-pygame
https://stackoverflow.com/questions/30418824/pygame-how-to-get-attack-controls-working
음악 넣기 / 화면에 text 띄우기)
https://futurestorys.tistory.com/102
https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

<hr>



https://repl.it/@james1990a/UnselfishJoyfulDecimals

## Commit TEST