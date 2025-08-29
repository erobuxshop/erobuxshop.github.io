#!/bin/bash

cd app/src/main/

# Компилируем Java код
ecj -cp /data/data/com.termux/files/usr/share/java/android-21.jar -d obj java/com/example/lightmessenger/*.java

# Создаем dex файл
dx --dex --output=classes.dex obj/

# Создаем ресурсы
aapt package -f -M AndroidManifest.xml -S res -I /data/data/com.termux/files/usr/share/java/android-21.jar -F app.apk.unaligned

# Добавляем классы в APK
aapt add app.apk.unaligned classes.dex

# Выравниваем APK
zipalign -f 4 app.apk.unaligned app.apk

# Переносим APK в корень
mv app.apk ../../../LightMessenger.apk

echo "Сборка завершена! APK: LightMessenger.apk"
