<html>
<head>
</head>
<body>
<p>I wanted to explore some internal processs communication methods and that led to me just writing an entire master and slave parallelization package utilizing sockets as a communication mechanism between processes.  From what I've read, some of the techniques employed here are very similar to <a href="https://github.com/zeromq/pyzmq">Zero MQ</a>.  That being said, it has been enjoyable and ensightful to build.  Feel free to play around!</p>

<br>
<label>Example:
<code>from sockproc import serversock<br>
      # host and port for the master socket
      master = serversock.MasterProcess('127.0.0.1', 8000)
      master.setup()
      master.handle_connections()
</code>
<br>
<p>In a separate interpreter:
<br>
<code>from sockproc import spawn<br>
      procs = spawn.Processes(2, func, args)
      procs.run()
</code>
</body>
</html>
