import math

#Artificial wall data
#This is a wall library that normally we get these walls from Revit- We created here to test artificially
#The difference between the artificial wall library and the ones we take from revit that when we collect the walls from revit, based on our demand we should add the filtering process


walls = [
    {"id": "W1", "length_mm": 4200, "height_mm": 2700, "has_framing_type": True},
    {"id": "W2", "length_mm": 3000, "height_mm": 2700, "has_framing_type": False},
    {"id": "W3", "length_mm": 5400, "height_mm": 2700, "has_framing_type": True},
]

#?????we can get wall informations, parameters, properties as a dictionary format from revit? OR should we build it when we collect the data? How can/should we structure the data?
#Answer:  We need to build the data structure after we collect and filter

#QA Function
#Here we already have bunch of data about the elements(walls) so, we need to determine the rules, limits, so we need to check  how the data is
#For example, length, height can not be smaller than 0. If there is no framing type, we can not test it.
#QA can be 4 groups: "Data Completeness: Bigi var mı?/Tanımlı mı" - "Geometry Sanity: boyut mantıklı mı? geometri uyusuyor mu düz mu vs. cok kısa/uzun parcalar" - "relational: diğer bim elemanları ile kontrol mep, aralarındaki boyutsal ilişki/yakınlık uzaklık/acıklıklar, köşeler, grid level ilişkisi, "
# " - "consistency: aynı seyler aybnı mı? parametreler, kopyalanan elemanlar, duplicate elemanlar, ID/Mark clash var mı?"

#??? how can we build all these controls? groups? dictio? data structure? if elses? what is the best way to do? what is the best way to build these questions and organize
#Cevap: her bir kategoriyi ayrı bir def fonksiyonu olarak tanımlayıp içeride if-else donguleri olustur
#En son baska bir check_wall fonksiyonu olustur. Ve içindeki genel/toplamı gosteren issues listesine farklı kategorilerin issues listeleri ekle tek tek.-
# temiz bir data structure cıktıgında sonrasında gorsellestirme ve grafikleri olsuturabilirsin  


def check_wall(wall):
    if not wall["has_framing_type"]:
        return False, "Framing type missing"
    elif wall["length_mm"] <= 0:
        return False, "the length value should be bigger than 0"
    elif wall["height_mm"] <= 0:
        return False, "the height value should be bigger than 0"
    return True, "Ok"

#Passed_wall_list_create
#passed walls kısmına derecelendirmeler koyulabilir  ya da issue leri derecelendirerek raporda sunulabilir
####"Kurallar gerçekte üreticiden gelir. Bu yüzden aracı, kullanıcının kural yazdığı değil, 
# hazır kural profilleri arasında seçim yaptığı bir yapıda kurdum. Gerçek bir projede bu 
# profiller üreticinin dokümanından doldurulur; burada temsili değerler kullandım."
##Gerçek dünyada analojisi şu: bir mimar duvar tipini kendisi icat etmez, üreticinin kataloğundan seçer. 
##Senin aracın da aynı şekilde çalışmalı — içinde birkaç hazır "kural profili" olur, mimar aralarında geçiş yapar ve farkı görür


##"bu araç kime hitap ediyor" diye takılmıştık. Cevap şu: fabrikatör henüz seçilmemişken, mimarın farklı üretim yaklaşımlarının sonuçlarını görebilmesi.
##"Eğer 400mm aralıklı bir sistemle çalışan bir üreticiyle gidersem şu, 600mm ile çalışanla gidersem bu" — bu, gerçek ve savunulabilir bir karar anı.

passed_walls = []



#Burada yapılan şey üst tarafta duvarları test etmek amacıyla olusturulan fonksiyonun içine elimizdeki duvar listesindeki duvarları tek tek atıp sonuc almak. Ve sonuc(passed) true ise bu duvarları bir
#listede toplamak ve butun fonksiyona giren duvarları passed durumu ve mesajı ve id si ile beraber basmak(print)
#testing function for the wall list
for wall in walls:
    passed, message = check_wall(wall)
    print(f"{wall['id']}: passed={passed}, message={message}")
    if passed:
        passed_walls.append(wall)

print(passed_walls)
#testi gecen duvarların basılması

#buradaki rule A ve rule B aslında gercek tool un akısında 2 farklı üreticinin verileri kuralları limitlerini iceren iki farklı json dosyası(json dosyaları bir cesit dict yapısında- biz
#dicti su an burada en basit haliyle rule A ve rule B olarak kurduk. Bu dict ler dısarıdan alınan veriler kurallar olacak - üretici firmanın kendi kuralları gibi bir mantıkla- outsource)
#core icin değil ama olası AI entegrasyonu için şöyle bir modul eklenebilir: Her üreticinin teknik pdf dokumanı vs nin antropic AI API baglanarak burada o dokuman okutulup 
#bu dokumandan structured data cıkarımı- json ı otomatik olusturma yapılabilir. Ama burada onemli olan şey, bu datanın dogrudan kullanılmaması, null methodu ile bilinmeneyen bulunmauan 
#datanın ai tarafından saçma veriler ile doldurulmasının önüne geçilmesi. Bunun için ai a sacmalama, uydurma gibi komutlar kullanılması, gelen doldurulan verinin kaynagaının mumkun oldugunca kontrol edilebilir olması
#ve en son otomatik doldurmadan once kullanıcının bu verileri gorebiliyor check edebiliyor ve gerekirse manuel mudehale edebiliyor olması(bu workflow ile bir calculation yapıldıgfında bunu manuel de test edip
#sonucları kıyasla)- bu asama da dahil genel olarak toolunun yaptıgı isi manuel de yaparak somut bir istatistiksel veri cıkart ve bu veriyi- sağladıgın verimlilik olarak sun 
#Some Rules for fab test
#buradaki rule dediğimiz şeyler aslında outsource gelen manufacturer ın standartları, size panel thickness max sizes min sizes stud spacing gibi farklı üreticilerdenn gelen farklı boyut limit standart veriler
#yani rule dediğimiz sey aslında aksiyonu ya da fonksiyonu belirlemiyor. Rule üreticiden gelen kısıtlar
RULE_A = {"name": "Standard", "stud_spacing_mm": 400, "panel_width_mm": 1200}
RULE_B = {"name": "Wide spacing", "stud_spacing_mm": 600, "panel_width_mm": 2400}


#elimizdeki wallerın parametreleri, özellikleri degerleri ve üretici katalogundan gelen kısıtların bir araya gelerek bir hesaplama yapılması ve bu hesaplama sonucunda
#benim elimdeki pre manufactıring sonucun elde edilmesi(stud sayısı, uniq panels...etc) Bunun gibi iliskiler kurularak pek cok fonksiyon yazılabilir ve hesaplama yaptırılabilir.
#????Baska üretim öncesi nasıl bir cıktı olusturabiliriz? Yoksa diğer türlüsü aslında hesap makinesi ya da counter?? Bu kısmı ne kadar faydalı?
#cevap:Bu tam olarak sorulması gereken soru. Ve cevap şu: sayma işleminin kendisi değersiz, sayma sonucunda ortaya çıkan karşılaştırma ve uyarı değerli. Ama haklısın — mevcut hesaplar bir tool'u haklı çıkarmaz. Gerçekte neyin hesaplanması gerektiğini kategorilere ayırayım.
#Kategori 1 — Fizibilite (evet/hayır soruları)
#Bunlar sayı üretmez, karar üretir. Ve mimara en somut faydayı bunlar sağlar.
#Bu duvar üretilebilir mi? Panel max uzunluğunu/yüksekliğini aşıyor mu?
#Ağırlık limitini aşıyor mu? (panel alanı × malzeme yoğunluğu → vinç/taşıma kapasitesi)
#Taşıma genişliğine sığıyor mu?
#Açıklık, panel kenarına framing için gereken minimum mesafeden yakın mı?
#İki açıklık arasına dikme sığıyor mu?
#Duvar, minimum üretilebilir uzunluğun altında mı? (10cm'lik bir panel üretilmez)
#Bunlar "bu tasarımı bu üreticiyle yapamazsın" der. Bir mimar için "kaç dikme" bilgisinden kat kat değerlidir, çünkü doğrudan tasarımı değiştirir.
#Kategori 2 — Tekrar ve çeşitlilik (modüler işin kalbi)
#Modüler inşaatın bütün ekonomisi burada. Ve bu, sayma değil sınıflandırma.
#Kaç benzersiz panel tipi var? (1200 duvar → 43 tip mi, 380 tip mi?)
#Tip başına kaç adet? (üretim serisi uzunluğu — 50 adetlik seri, 1 adetlik özelden çok daha ucuz)
#Sadece bir kez kullanılan kaç tip var? (bunlar maliyet katilidir)
#Küçük bir tolerans gevşetsem kaç tip birleşir? (4200 ve 4210'u aynı sayarsam 5 tip azalıyor gibi)
#Son madde özellikle güçlü, çünkü mimara eyleme geçirilebilir bir şey söyler: "şu üç duvarı 10mm ayarlarsan bir tip azalır."
#Kategori 3 — Malzeme verimliliği (asıl waste burada)
#Şu anki panel sayımı fire hesaplamıyor. Gerçek hesap şu:
#Stok levha ebadından kaç panel çıkar, ne kadar artar?
#Farklı stok ebatları denenirse hangisi en az fire verir?
#Kesim parçaları başka bir panelde kullanılabilir mi? (bu, nesting problemi)
#Dikme profilleri standart boyda geliyorsa, kesim planı ne kadar hurda bırakıyor?
#Bunun için available_lengths_mm gibi gerçek stok verisi gerekir — daha önce konuştuğumuz JSON yapısındaki alan tam bunun için.
#Kategori 4 — Karmaşıklık göstergeleri
#Üretim maliyeti sadece miktara bağlı değil, karmaşıklığa da bağlı.
#Panel başına açıklık sayısı (0 açıklıklı panel hızlı üretilir, 3 açıklıklı yavaş)
#MEP geçişi olan panel oranı
#Standart dışı boyutlu panel oranı
#Panel başına farklı malzeme tipi sayısı
#Bunlar "bu proje ne kadar zor" sorusunun sayısal karşılığı.
#Kategori 5 — Duyarlılık analizi (en ilginç olanı)
#Tek bir sonuç değil, değişime tepki ölçmek:
#Kural profili A yerine B seçilirse toplam ne kadar değişir?
#Panel max uzunluğu 6000 yerine 4800 olsa (farklı üretici) kaç panel eklenir?
#Duvar yüksekliği 2700'den 3000'e çıksa kaç tip etkilenir?
#Bu, aracın "hesap makinesi"nden "karar destek aracı"na dönüştüğü yer. Ve senin mevcut kural karşılaştırma yapın zaten bunun tohumu.
#Peki hangisini yapmalısın
#Hepsini değil. Şu üçü, birlikte, gerçekten savunulabilir bir araç oluşturur:
#Fizibilite bayrakları (Kategori 1) — en somut fayda, en kolay uygulama. Tip sınıflandırma (Kategori 2) — en ayırt edici, sektörde en az çözülmüş. Fire hesabı (Kategori 3) — vaat ettiğin sayı, stok verisiyle mümkün.
#Bunlar birleştiğinde çıktı şuna dönüşür: "1200 duvar, 43 tip, 6 tanesi üretilemez (max uzunluk aşımı), %12 fire, Profil B ile %8 fire." Bu, bir mimarın gerçekten bakacağı bir rapor.
#Neden şu anki basit hesap yine de gerekliydi
#Çünkü yukarıdaki her şey aynı iskelet üzerine kuruluyor: duvar verisi + kural profili → fonksiyon → sonuç. Sen o iskeleti kurdun ve anladın. Şimdi fonksiyonların içi zenginleşecek, mimari değişmeyecek.
#Sıradaki adım olarak fizibilite bayraklarını eklemeyi öneririm — kural profiline max_panel_length_mm koyup, calculate_wall_fab'a "bu duvar limiti aşıyor mu" kontrolü eklemek.

def calculate_wall_fab(wall, rule):
    stud_count = math.ceil(wall["length_mm"] / rule["stud_spacing_mm"]) + 1
    panel_count = math.ceil(wall["length_mm"] / rule["panel_width_mm"])
    return {"wall_id": wall["id"], "stud_count": stud_count, "panel_count": panel_count}

rejected_count = len(walls) - len(passed_walls)
print(f"Rejected walls: {rejected_count}")


#her bir gelen json dosyası- 2 farklı üretici kısıt dosyasını tek tek calıstırmak için bir listeye koyup for dongusu yaptık. Bu for dongusu içinde
#olsuturdugumuz fonksiyonları her bir duvar icin uygulayacagız rule ve wall ı kullandık ve sonucları her bir uretici kısıt json u/dict i için yazdırdık.
rules = [RULE_A, RULE_B]
for rule in rules:
    total_studs = 0
    total_panels = 0
    for wall in passed_walls:
        result = calculate_wall_fab(wall, rule)
        total_studs += result["stud_count"]
        total_panels += result["panel_count"]
    print(f"{rule['name']}: total studs={total_studs}, total panels={total_panels}")
