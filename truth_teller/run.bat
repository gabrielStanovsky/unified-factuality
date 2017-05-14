@echo off

set JAVA_HOME=java\windows\jdk1.7.0_06

set CLASSPATH=jars\common-1.0.1-SNAPSHOT.jar
set CLASSPATH=%CLASSPATH%;jars\lap-1.0.1-SNAPSHOT.jar
set CLASSPATH=%CLASSPATH%;jars\core-1.0.1-SNAPSHOT.jar
set CLASSPATH=%CLASSPATH%;jars\log4j-1.2.17.jar
set CLASSPATH=%CLASSPATH%;jars\stanford-postagger-2008-09-28.jar
set CLASSPATH=%CLASSPATH%;jars\transformations-1.0.1-SNAPSHOT.jar
set CLASSPATH=%CLASSPATH%;jars\lingpipe-3.1.1.jar
rem set CLASSPATH=%CLASSPATH%;jars\

echo %*
"%JAVA_HOME%\bin\java" eu.excitementproject.eop.transformations.generic.truthteller.conll.AnnotateSentenceToConll configuration.xml %*

