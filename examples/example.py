import captcha

phrase, image = captcha.new('portuguese')

print(phrase)
image.show()