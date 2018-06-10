
IF EXIST galleryLinks.opml (
    Echo The file was not found.	
 ) ELSE ( 
 copy galleries.opml galleryLinks.opml
    
 )

for /f "delims=" %%i in (D:\Developed\Automation\GalleryDownloader\heartQueens.txt) do xcopy C:\GalImgs\NewBabes\*%%i* C:\GalImgs\chosen\ && del /q/f C:\GalImgs\NewBabes\*%%i*
dir /b "C:\GalImgs\chosen\*.jpg"  >> galleryLinksTemp.txt
::del /q/f galleryLinks.opml
::copy galleries.opml galleryLinks.opml
for /f "delims=^." %%i in (galleryLinksTemp.txt) do echo http://babesource.com/galleries/%%i.html>> "D:\Developed\Automation\GalleryDownloader\galleryLinks.opml"
del /q/f galleryLinksTemp.txt
rd /s/q C:\GalImgs\chosen
md C:\GalImgs\chosen
