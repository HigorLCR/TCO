def reverse_string(s):
    if s == "":
        return ""
    else:
        return reverse_string(s[1:]) + s[0]
    

print(reverse_string("Luza Rocelina, a namorada do Manuel, leu na moda da Romana: anil é cor azul."))