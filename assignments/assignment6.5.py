#Write code using find() and string slicing (see section 6.10) to extract the number at the end of the line below. Convert the extracted value to a floating point number and print it out.

#line="From bergeroso@bergerium.com 6.5.2099"
#at_sign_posit=line.find("@")
#space_posit=line.find('',at_sign_posit)
#host=line.find[at_sign_posit+1:space_posit]
#print host

text = "X-DSPAM-Confidence:    0.8475";
#no_position=text.find("0")
blank_posit=text.find(" ")
#print no_position
#print blank_posit
#no_extr=text[no_position:]
no_extr=text[blank_posit:].lstrip()
#print no_extr
print float(no_extr)


