import os
import random 
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH <rct.right:  # 横方向のはみ出しチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向のはみ出しチェック
        tate = False
    return yoko, tate

# 演習1：ゲームオーバー画面
def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に
    「Game Over」の文字と，泣いているこうかとん画像を並べて表示する
    引数 screen：画面Surface
    """
    # 黒い半透明のSurface
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.set_alpha(200)
    black_sfc.fill((0, 0, 0))
    
    # 「Game Over」の文字
    fonto = pg.font.Font(None, 80)
    txt_sfc = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_sfc.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    
    # 泣いているこうかとん画像
    kk_img = pg.image.load("fig/8.png") 
    kk_rct1 = kk_img.get_rect()
    kk_rct1.center = WIDTH // 2 - 200, HEIGHT // 2 
    kk_rct2 = kk_img.get_rect()
    kk_rct2.center = WIDTH // 2 + 200, HEIGHT // 2 
    
    # 描画
    screen.blit(black_sfc, (0, 0)) 
    screen.blit(txt_sfc, txt_rct)  
    screen.blit(kk_img, kk_rct1)   
    screen.blit(kk_img, kk_rct2)   
    
    pg.display.update()
    time.sleep(5)

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す辞書
    戻り値：キーが移動量タプル、値がrotozoomされたSurfaceの辞書
    """
    kk_img = pg.image.load("fig/3.png")
    kk_imgs = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),    # 左
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 0.9),  # 左下
        (0, +5): pg.transform.rotozoom(kk_img, 90, 0.9),   # 下
        (+5, +5): pg.transform.rotozoom(kk_img, 135, 0.9), # 右下
        (+5, 0): pg.transform.flip(kk_img, True, False),   # 右（反転）
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 0.9), # 右上
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 0.9),  # 上
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9), # 左上
    }
    return kk_imgs    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  

    # 演習3：こうかとん画像の辞書を取得
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)] 
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透過色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の横速度，縦速度
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        # 背景描画
        screen.blit(bg_img, [0, 0]) 

        # 衝突判定（ここで当たっていたらgameoverを呼ぶ）
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # キー入力とこうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  
                sum_mv[1] += mv[1]
        
        # 演習3：移動方向に応じてこうかとん画像を変更
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面内外の判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  

        # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()