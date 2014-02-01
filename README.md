<html>
<head>
</head>
<body>
<p>I wanted to explore some internal processs communication methods and that led to me just writing an entire master and slave parallelization package utilizing sockets as a communication mechanism between processes.  From what I've read, some of the techniques employed here are very similar to <a href="https://github.com/zeromq/pyzmq">Zero MQ</a>.  That being said, it has been enjoyable and ensightful to build.  Feel free to play around!</p>

<br>
<label>Example:<br>
<code>from sockproc import serversock<br>
</code>
<b>
<code># host and port for the master socket</code><br>
<code>master = serversock.MasterProcess('127.0.0.1', 8000)</code><br>
<code>master.setup()</code><br>
<code>master.handle_connections()</code><br>
</b>

<br>
<p>In a separate interpreter:
<br>
<b>
<code>from sockproc import spawn</code><br>
<code>procs = spawn.Processes(2, func, args)</code><br>
<code>procs.run()</code>
</b>
</body>
</html>
