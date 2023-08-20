import vocabularizer as v


#v.show_vocabulary(0,1000)
v.load_file(v.get_config("default_vocabulary"))
#v.save_vocabulary_to_file(v.get_config("default_vocabulary"))
#v.save_weights(v.get_config("weights_file"))
#v.unload_vocabulary()
# for i in range(1, 10):
#     v.load_file(v.get_config("default_vocabulary"))

#     v.unload_vocabulary()

#v.load_file(v.get_config("default_vocabulary"))
v.show_vocabulary(0,30)
v.save_weights(v.get_config("weights_file"))
v.save_vocabulary_to_file(v.get_config("default_vocabulary"))
v.unload_vocabulary()
v.load_file(v.get_config("default_vocabulary"))
#v.test_1()
v.show_vocabulary(0,1000)
