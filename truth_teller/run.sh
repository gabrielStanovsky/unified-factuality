#!/bin/bash
#JAVA_HOME=java/linux/jdk1.7.0_10
#export JAVA_HOME

CLASSPATH=jars/common-1.0.1-SNAPSHOT.jar:jars/lap-1.0.1-SNAPSHOT.jar:jars/core-1.0.1-SNAPSHOT.jar:jars/log4j-1.2.17.jar:jars/stanford-postagger-2008-09-28.jar:jars/transformations-1.0.1-SNAPSHOT.jar:jars/lingpipe-3.1.1.jar
export CLASSPATH

$JAVA_HOME/bin/java eu.excitementproject.eop.transformations.generic.truthteller.conll.AnnotateSentenceToConll configuration.xml $@

