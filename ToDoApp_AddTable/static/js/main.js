//削除
function delete_todo() {
    if (confirm("本当に削除しますか？")) {
        return true;
    } else {
        return false;
    }
}

//新規追加
function openCreateModal() {
    const modal = new bootstrap.Modal(document.getElementById("createModal"));
    modal.show();
}

//編集
// openEditModal(id)で指定されたIDの行を編集
function openEditModal(id) {
    // index.htmlの69行目<tr id="row{{ id }}">に対応
    const row = document.getElementById("row" + id);
    // モーダル上で記入又は選択欄を表示するためにindex.htmlの94行目以降の値を代入
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_name").value = row.querySelector(".name").textContent.trim(); //名前
    document.getElementById("edit_task").value = row.querySelector(".task").textContent.trim(); //タスク
    document.getElementById("edit_due_date").value = row.querySelector(".due_date").textContent.trim(); //期日

    // 取引形態のラジオボタン
    const rentBuyValue = row.querySelector(".rent_buy").textContent.trim();
    document.getElementById("edit_rent_buy_re").checked = (rentBuyValue === "賃貸");
    document.getElementById("edit_rent_buy_sa").checked = (rentBuyValue === "売買");
    document.getElementById("edit_rent_buy_ma").checked = (rentBuyValue === "管理");

    // 物件種類のラジオボタン
    const realEstateValue = row.querySelector(".real_estate").textContent.trim();
    document.getElementById("edit_real_estate_la").checked = (realEstateValue === "土地");
    document.getElementById("edit_real_estate_ho").checked = (realEstateValue === "戸建て");
    document.getElementById("edit_real_estate_ap").checked = (realEstateValue === "集合住宅");

    document.getElementById("edit_real_estate_name").value = row.querySelector(".real_estate_name").textContent.trim(); //物件名
    document.getElementById("edit_note").value = row.querySelector(".note").textContent.trim(); //備考
    // 上記の記入欄や選択欄をモーダル上に表示
    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();
}

