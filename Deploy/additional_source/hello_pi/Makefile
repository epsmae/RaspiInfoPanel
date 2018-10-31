all: apps

libs/ilclient/libilclient.a:
	$(MAKE) -C libs/ilclient

apps: libs/ilclient/libilclient.a
	$(MAKE) -C hello_video

clean:
	$(MAKE) -C hello_video clean

