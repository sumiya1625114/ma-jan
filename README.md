# ma-jan

![png](https://github.com/sumiya1625114/ma-jan/blob/main/img/sample/sample.png)

## Overview

個人的な勉強用のリポジトリです。  
麻雀ゲーム(東一局のみ/CPUツモ切りのみ)

お借りした画像素材
麻雀王国　麻雀素材
https://mj-king.net/sozai/

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.9.13     |

## 現状の問題
・リーチ後のカン (nakip_btn）  
現在できない  
実装するなら暗カンのみ、待ちが変わってはだめ、カンできるのはツモ牌のみ  

・食い変えの鳴きができてしまう  
チーで同じ筋切れないように  

・役判定未実装のため役なし和了ができてしまう  
役判定実装待ち  

## 実装予定

・和了時の詳細表示  
役、ハンスウ、点数の表示  

・役チェック関数  
待ちから役計算　その牌があがれるか確認できるように  

・役判定のリスト  
yakulist matilistと同じだけ作り、0と1で役つくか格納  
あたり牌チェックが　NO＝0　役なしあたり＝1　役ありあたり＝2（リーチ含）を返すように  
（現状全部2返す）  

・CPUの和了・鳴き処理

・CPUのAI

・東風戦


