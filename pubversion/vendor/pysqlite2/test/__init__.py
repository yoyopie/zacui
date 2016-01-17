�
���Uc           @   sl   d  d l  Z  d  d l Z d  d l j Z d e j f d �  �  YZ d �  Z d �  Z e	 d k rh e �  n  d S(   i����Nt   RegressionTestsc           B   s�   e  Z d  �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z	 d �  Z
 d	 �  Z d
 �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z RS(   c         C   s   t  j d � |  _ d  S(   Ns   :memory:(   t   sqlitet   connectt   con(   t   self(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   setUp   s    c         C   s   |  j  j �  d  S(   N(   R   t   close(   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   tearDown    s    c         C   s    |  j  j �  } | j d � d  S(   Ns   pragma user_version(   R   t   cursort   execute(   R   t   cur(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckPragmaUserVersion#   s    c         C   sT   t  j d d t  j �} z  |  j j �  } | j d � Wd  | j �  | j �  Xd  S(   Ns   :memory:t   detect_typess   pragma schema_version(   R   R   t   PARSE_COLNAMESR   R   R	   R   (   R   R   R
   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckPragmaSchemaVersion(   s    
c         C   s�   t  j d d d �} g  t d � D] } | j �  ^ q" } | d j d � xD t d � D]6 } | d j d g  t d � D] } | f ^ qx � qX Wx- t d � D] } | | j d | d	 � q� W| j �  d  S(
   Ns   :memory:t   cached_statementsi   i    s   create table test(x)i
   s   insert into test(x) values (?)t    s   select x from test(   R   R   t   xrangeR   R	   t   ranget   executemanyt   rollback(   R   R   t   xt   cursorst   i(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckStatementReset2   s    %4c         C   sc   |  j  j �  } | j d � |  j | j d d d � | j d � |  j | j d d d � d  S(   Ns    select 1 as "foo bar [datetime]"i    s   foo bars   select 1 as "foo baz"s   foo baz(   R   R   R	   t   assertEqualt   description(   R   R
   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckColumnNameWithSpacesA   s
    c         C   sj   t  j d � } g  } xD t d � D]6 } | j �  } | j | � | j d t | � � q" W| j �  d  S(   Ns   :memory:ii   s   select 1 x union select (   R   R   R   R   t   appendR	   t   strR   (   R   R   R   R   R
   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt#   CheckStatementFinalizationOnCloseDbI   s    c         C   s�   t  j d k  r d  St  j d � } | j d � | j d � y | j d � Wn t  j k
 rc n X| j d � y | j �  Wn! t  j k
 r� |  j d � n Xd  S(	   Ni   i   s   :memory:s3   create table foo(x, unique(x) on conflict rollback)s   insert into foo(x) values (1)s   insert into foo(x) values (2)s1   pysqlite knew nothing about the implicit ROLLBACK(   i   i   i   (   R   t   sqlite_version_infoR   R	   t   DatabaseErrort   committ   OperationalErrort   fail(   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckOnConflictRollbackW   s    c         C   s4   |  j  j d � |  j  j d � |  j  j d � d S(   sm   
        pysqlite would crash with older SQLite versions unless
        a workaround is implemented.
        s   create table foo(bar)s   drop table fooN(   R   R	   (   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt-   CheckWorkaroundForBuggySqliteTransferBindingsg   s    c         C   s   |  j  j d � d S(   s   
        pysqlite used to segfault with SQLite versions 3.5.x. These return NULL
        for "no-operation" statements
        t    N(   R   R	   (   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckEmptyStatementp   s    c         C   s   t  j d � } | j �  d S(   s	  
        With pysqlite 2.4.0 you needed to use a string or a APSW connection
        object for opening database connections.

        Formerly, both bytestrings and unicode strings used to work.

        Let's make sure unicode strings work in the future.
        u   :memory:N(   R   R   R   (   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckUnicodeConnectw   s    	c         C   s�   d } t  j d d t  j �} | j d � | j d t j j �  f � | j | � | j d � | j d � | j d � | j | � d	 S(
   s�   
        pysqlite until 2.4.1 did not rebuild the row_cast_map when recompiling
        a statement. This test exhibits the problem.
        s   select * from foos   :memory:R   s   create table foo(bar timestamp)s   insert into foo(bar) values (?)s   drop table foos   create table foo(bar integer)s   insert into foo(bar) values (5)N(   R   R   t   PARSE_DECLTYPESR	   t   datetimet   now(   R   t   SELECTR   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckTypeMapUsage�   s    c         C   s   |  j  t t j i  d � d S(   s!   
        See issue 3312.
        N(   t   assertRaisest	   TypeErrorR   t   register_adaptert   None(   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckRegisterAdapter�   s    c         C   s,   t  j d � } |  j t t | d d � d S(   s!   
        See issue 3312.
        s   :memory:t   isolation_levelu   éN(   R   R   R.   t   UnicodeEncodeErrort   setattr(   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckSetIsolationLevel�   s    c         C   s�   d t  j f d �  �  Y} t  j d � } | | � } y$ | j d � j �  |  j d � Wn' t  j k
 rn n |  j d � n Xd S(   s[   
        Verifies that cursor methods check wether base class __init__ was called.
        t   Cursorc           B   s   e  Z d  �  Z RS(   c         S   s   d  S(   N(    (   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   __init__�   s    (   t   __name__t
   __module__R8   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR7   �   s   s   :memory:s
   select 4+5s#   should have raised ProgrammingErrorN(   R   R7   R   R	   t   fetchallR#   t   ProgrammingError(   R   R7   R   R
   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckCursorConstructorCallCheck�   s    c         C   sp   d t  j f d �  �  Y} | d � } y | j �  } |  j d � Wn' t  j k
 rX n |  j d � n Xd S(   s_   
        Verifies that connection methods check wether base class __init__ was called.
        t
   Connectionc           B   s   e  Z d  �  Z RS(   c         S   s   d  S(   N(    (   R   t   name(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR8   �   s    (   R9   R:   R8   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR>   �   s   s   :memory:s#   should have raised ProgrammingErrorN(   R   R>   R   R#   R<   (   R   R>   R   R
   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt#   CheckConnectionConstructorCallCheck�   s    c            s�   d t  j f �  f d �  �  Y} d t  j f d �  �  Y�  | d � } | j �  } | j d � | j d d d d g � | j d � | j �  y | j �  |  j d � Wn' t  j	 k
 r� n |  j d � n Xd S(   s�   
        Verifies that subclassed cursor classes are correctly registered with
        the connection object, too.  (fetch-across-rollback problem)
        R>   c              s   e  Z �  f d  �  Z RS(   c            s
   �  |  � S(   N(    (   R   (   R7   (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR   �   s    (   R9   R:   R   (    (   R7   (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR>   �   s   R7   c           B   s   e  Z d  �  Z RS(   c         S   s   t  j j |  | � d  S(   N(   R   R7   R8   (   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR8   �   s    (   R9   R:   R8   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR7   �   s   s   :memory:s   create table foo(x)s   insert into foo(x) values (?)i   i   i   s   select x from foos!   should have raised InterfaceErrorN(   i   (   i   (   i   (
   R   R>   R7   R   R	   R   R   R;   R#   t   InterfaceError(   R   R>   R   R
   (    (   R7   sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckCursorRegistration�   s    

c         C   s   t  j d d d �} d S(   s�   
        Verifies that creating a connection in autocommit mode works.
        2.5.3 introduced a regression so that these could no longer
        be created.
        s   :memory:R3   N(   R   R   R1   (   R   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckAutoCommit�   s    c         C   sR   t  j d � } | j �  } | j d � | j d � | j d � | j �  } d S(   s�   
        Verifies that running a PRAGMA statement that does an autocommit does
        work. This did not work in 2.5.3/2.5.4.
        s   :memory:s   create table foo(bar)s   insert into foo(bar) values (5)s   pragma page_sizeN(   R   R   R   R	   t   fetchone(   R   R   R
   t   row(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckPragmaAutocommit�   s    c         C   s�   d d d �  �  Y} | �  } t  j d � } |  j t | j | � |  j t | j | � |  j t | j | � |  j t | j | � d S(   s�   
        See http://bugs.python.org/issue7478

        It was possible to successfully register callbacks that could not be
        hashed. Return codes of PyDict_SetItem were not checked properly.
        t   NotHashablec           B   s   e  Z d  �  Z d �  Z RS(   c         _   s   d  S(   N(    (   R   t   argst   kw(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   __call__�   s    c         S   s   t  �  � d  S(   N(   R/   (   R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   __hash__�   s    (   R9   R:   RJ   RK   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyRG   �   s   	s   :memory:N(    (   R   R   R.   R/   t   create_functiont   create_aggregatet   set_authorizert   set_progress_handler(   R   RG   t   varR   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckSetDict�   s    	c            s�   t  j d � } | j �  �  �  j d � �  j d � �  f d �  } y. �  j d d �  | �  D� � |  j d � Wn t  j k
 r� n Xd S(	   s�   
        http://bugs.python.org/issue10811

        Recursively using a cursor, such as when reusing it from a generator led to segfaults.
        Now we catch recursive cursor usage and raise a ProgrammingError.
        s   :memory:s   create table a (bar)s   create table b (baz)c           3   s   �  j  d d � d Vd  S(   Ns   insert into a (bar) values (?)i   (   i   (   R	   (    (   R
   (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   foo  s    s   insert into b (baz) values (?)c         s   s   |  ] } | f Vq d  S(   N(    (   t   .0R   (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pys	   <genexpr>  s    s#   should have raised ProgrammingErrorN(   R   R   R   R	   R   R#   R<   (   R   R   RR   (    (   R
   sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   CheckRecursiveCursorUse  s    (   R9   R:   R   R   R   R   R   R   R   R$   R%   R'   R(   R-   R2   R6   R=   R@   RB   RC   RF   RQ   RT   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyR       s*   				
																	c          C   s"   t  j t d � }  t  j |  f � S(   Nt   Check(   t   unittestt	   makeSuiteR    t	   TestSuite(   t   regression_suite(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   suite  s    c          C   s    t  j �  }  |  j t �  � d  S(   N(   RV   t   TextTestRunnert   runRZ   (   t   runner(    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   test!  s    t   __main__(
   R*   RV   t   pysqlite2.dbapi2t   dbapi2R   t   TestCaseR    RZ   R^   R9   (    (    (    sM   /usr/local/python2.7/lib/python2.7/site-packages/pysqlite2/test/regression.pyt   <module>   s   � 		