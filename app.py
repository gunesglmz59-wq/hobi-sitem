from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veriler.db"
db = SQLAlchemy(app)


class KulllaniciHobi(db.Model):                     #kullanıcı hobi listesi olustu
    id = db.Column(db.Integer, primary_key = True)  #sıra no         
    isim = db.Column(db.String(50))                 #sütun baslıgı
    hobi = db.Column(db.String(100))                #ikinci sutun baslıgı


with app.app_context():         #db ile işlem yapıcaksan context e girmen lazım
    db.create_all()             #class şablonuna bakıp klasörde veriler.db dosyası olusturur


@app.route("/")                                                 #eger kullanıcı sadece/ yazarsa asagıdaki fonk u calıstır
def ana_sayfa():
    tum_hobiler = KulllaniciHobi.query.all()                    #kullancicihobi database den tum kayıtları liste halinde getir
    return render_template("index.html", hobiler= tum_hobiler)  #tum_hobiler gecici sepetine html de hobiler ismini verdi


@app.route("/cevap", methods=["POST"])                          
def cevap():        #kullanıcı gönder e baastıgında calısır
    # HTML formundaki 'name' etiketlerine göre verileri çekiyoruz
    ad= request.form.get("mesaj") # paketteki mesaj etiketini bulup al. (html de <input name= "mesaj" kısmı)
    yeni_hobi = request.form.get("hobi")    

    yeni_kayit = KulllaniciHobi(isim= ad, hobi = yeni_hobi)
    db.session.add(yeni_kayit)
    db.session.commit()         #mühürleme

    return redirect("/")

    
@app.route("/sil/<int:id>")
def sil(id):
    silinecek_kayit = KulllaniciHobi.query.get(id)
    if silinecek_kayit:
        db.session.delete(silinecek_kayit)
        db. session.commit()
    return redirect("/")


@app.route("/guncelle_hazirlik", methods=["POST"])
def guncelle_hazirlik():
    id = request.form.get("id")
    kayit = KulllaniciHobi.query.get(id)
    # Veriyi bulup "guncelle.html" diye yeni bir sayfaya gönderiyoruz
    return render_template("guncelle.html", kayit=kayit)


@app.route("/guncelle/<int:id>", methods= ["POST"])
def guncelle(id):
    kayit = KulllaniciHobi.query.get(id)
    if kayit:
        yeni_isim= request.form.get("yeni_isim")
        yeni_hobi = request.form.get("yeni_hobi")

        kayit.isim = yeni_isim      #eski kayıt dosaysının isim bölümünü sil yeni_isim i yaz
        kayit.hobi = yeni_hobi

        db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)