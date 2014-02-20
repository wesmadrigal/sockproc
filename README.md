<html>
<head>
</head>
<body>
<p>I wanted to explore some internal processs communication methods and that led to me just writing an entire master and slave parallelization package utilizing sockets as a communication mechanism between processes.  From what I've read, some of the techniques employed here are very similar to <a href="https://github.com/zeromq/pyzmq">Zero MQ</a>.  That being said, it has been enjoyable and insightful to build.  Feel free to play around!</p>

<br>
<label>Example:<br>
<code>from sockproc.serversock import MasterProcess<br>
</code>
<b>
<code># host and port for the master socket</code><br>
<code># the port 8000 I used is arbitrary</code><br>
<code>master = serversock.MasterProcess('127.0.0.1', 8000)</code><br>
<code>master.setup()</code><br>
<code>master.handle_processes()</code><br>
</b>

<br>
<p>In a separate interpreter:
<br>
<b>
<code>from sockproc.spawn import Pool</code><br>
<code># args are a tuple (arg1, arg2, arg3,)</code><br>
<code>pool = Pool(2, func, args)</code><br>
<code>pool.run()</code>
</b>
</body>
</html>
