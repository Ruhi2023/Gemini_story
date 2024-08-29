def gen_text(d):
    #login and connfigure google model for text
    import google.generativeai as gai 
    gai.configure(api_key=d['ugak'])
    generation_config = {
          "temperature": 0.9,
          "top_p": 0.95,
          "top_k": 64,
          "max_output_tokens": 8192,
          "response_mime_type": "text/plain",
        }
        
    model = gai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
    print("Trying to generate text......")
    res = model.generate_content(d['prompt'])
    
    print("Text Generated!!")
    output= res.text
    print(output)
    if all(sub in output for sub in ["tx", "ctx", "stx"]):
        ind_tx = output.index("tx")
        ind_ctx = output.index("ctx")
        ind_stx = output.index("stx")
        if output.rfind("}")>8:
            ind_la = output.rfind("```")
        else:
            ind_la = output.rfind("}")
        li = [ind_tx,ind_ctx,ind_stx,ind_la]
        li.sort()
        #slices
        slL = []
        d2 ={}
        
        for i in range(0,len(li)-1):
            a = li[i]-1
            b = li[i+1]-1
            sl = output[a:b]
            sl =sl.strip()
            sl = sl.removesuffix(",")
            sl = sl.replace('""','"')
            slL.append(sl)
        keys =[]
        for i in slL:
            nel=i.split('":')
            nel[1] = nel[1].strip()
            d2[nel[0]]=nel[1]
            keys.append(nel[0])
        d2['keys']=keys
        print(d2['keys'])
        return d2

