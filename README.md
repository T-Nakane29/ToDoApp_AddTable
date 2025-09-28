# 不動産会社向けタスク管理アプリ
## ◎作成理由
### 経験上、多くの種類のタスクが混在するため、タスクの抜け漏れ改善のため。
##
## ◎工夫点
### 学習のために編集・削除機能の実装や顧客テーブルの作成に挑戦しました。
## 
## ◎主な機能
### タスクの追加・編集・削除
### PC画面での業務一覧表示
## 
## ◎技術スタック
### Pythonバージョン：Python 3.13.5
### フレームワーク：Flask
### 主要ライブラリ：Flask, render_template, request, redirect, session, settings, os
## 
## ◎セットアップ手順
#### ※①～③に関しては使用PCに合うものをインストールすること 
#### ①Visual Studio Codeを下記URLからインストール 
####  https://code.visualstudio.com/ 
#### ②Pythonを下記URLからインストール 
####  https://www.python.org/downloads/ 
#### ③MariaDBを下記URLからインストール 
####  https://mariadb.org/ 
#### ④PCの検索から以下のプログラムを検索し、選択する
#### <img width="363" height="108" alt="image" src="https://github.com/user-attachments/assets/0baeb5b4-1cda-4e8e-9024-ac97f943f8ad" />
#### ⑤③でインストール時に設定したパスワードを入力し｢INSERT INTO users (name) VALUES ('中根 貴仁');｣と入力
#### ⑥コマンドプロントを開き、
#### 「pip install flask」と記入してEnterを押しFlaskをインストール
#### 「pip install mysql-connector-python」と記入してEnterを押しインストール
####  上記と同様に主要ライブラリをインストール
#### ⑦タスク管理アプリのファイル上で右クリックをしてCodeで開くを選択 
#### ⑧開いた画面の左側のmain.pyを選択 
#### ⑨コードが記載された画面(右側)で右クリックをしてPythonの実行からターミナルでPythonファイルを実行するを選択 
#### ⑩Python実行後、下段のコマンドプロントに表示された下記URLでCtrl＋クリック を行い、ブラウザ（Microsoft Edge ）でタスク管理アプリを開いておく
#### http://127.0.0.1:2000/ 
## 
## ◎使用方法
### ※初期利用及び新規ユーザー登録について
### ①ログイン時に｢中根 貴仁｣と記入
### ②ログイン後にユーザー登録ボタンを押し、使用する方の名前を入力し登録ボタンを押す
### <img width="125" height="54" alt="image" src="https://github.com/user-attachments/assets/2afe3340-a6a5-4924-b0cc-262d0476086d" />
### <img width="484" height="184" alt="image" src="https://github.com/user-attachments/assets/57343ddf-5330-4ddc-b0ba-e77b10a288d1" />
### ●新規タスク登録から一覧表示 
#### ①一覧画面より新規タスク登録ボタンを選択 
#### ②新規タスク入力画面にて条件の値を記入及び選択 
#### ③登録ボタンを選択 
### ●編集から一覧表示 
#### ①一覧画面より編集するタスクの編集ボタンを選択 
#### ②タスク編集画面にて値を条件の値に変更及び選択 
#### ③保存ボタンを選択 
### ●削除から一覧表示 
#### ①一覧画面より削除するタスクの削除ボタンを選択 
#### ②ホップアップで表示された画面のOKボタンを押す 

   
