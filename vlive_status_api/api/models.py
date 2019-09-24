from django.db import models

# Create your models here.

class Vtuber(models.Model):
	GENDER = (('man', '男性'),
			  ('woman', '女性'),
			  ('etc', 'その他')
			  )
	PRODUCTION = (('hololive', 'ホロライブ'),
				  ('nijisanji','にじさんじ'),
				  ('upd8','upd8'),
				  ('dotlive','.Live'),
				  ('react', 'Re:Act'),
				  ('etc','その他')
				  )

	uid = models.CharField(max_length=50, primary_key=True)
	liver_name = models.CharField(max_length=100)
	production = models.CharField(max_length=100, choices=PRODUCTION)
	gender = models.CharField(max_length=20, choices=GENDER)


class On_Live(models.Model):
	uid = models.ForeignKey(Vtuber, on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now_add=True)
	live_title = models.CharField(max_length=100)

