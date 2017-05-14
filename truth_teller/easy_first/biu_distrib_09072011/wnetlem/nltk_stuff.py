# source: Natural Language Toolkit: WordNet
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Steven Bethard <Steven.Bethard@colorado.edu>
#         Steven Bird <sb@csse.unimelb.edu.au>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
import re

from data import FileSystemPathPointer, ZipFilePathPointer
class CorpusReader(object):
    """
    A base class for X{corpus reader} classes, each of which can be
    used to read a specific corpus format.  Each individual corpus
    reader instance is used to read a specific corpus, consisting of
    one or more files under a common root directory.  Each file is
    identified by its C{file identifier}, which is the relative path
    to the file from the root directory.

    A separate subclass is be defined for each corpus format.  These
    subclasses define one or more methods that provide 'views' on the
    corpus contents, such as C{words()} (for a list of words) and
    C{parsed_sents()} (for a list of parsed sentences).  Called with
    no arguments, these methods will return the contents of the entire
    corpus.  For most corpora, these methods define one or more
    selection arguments, such as C{fileids} or C{categories}, which can
    be used to select which portion of the corpus should be returned.
    """
    def __init__(self, root, fileids, encoding=None, tag_mapping_function=None):
        """
        @type root: L{PathPointer} or C{str}
        @param root: A path pointer identifying the root directory for
            this corpus.  If a string is specified, then it will be
            converted to a L{PathPointer} automatically.
        @param fileids: A list of the files that make up this corpus.
            This list can either be specified explicitly, as a list of
            strings; or implicitly, as a regular expression over file
            paths.  The absolute path for each file will be constructed
            by joining the reader's root to each file name.
        @param encoding: The default unicode encoding for the files
            that make up the corpus.  C{encoding}'s value can be any
            of the following:

              - B{A string}: C{encoding} is the encoding name for all
                files.
              - B{A dictionary}: C{encoding[file_id]} is the encoding
                name for the file whose identifier is C{file_id}.  If
                C{file_id} is not in C{encoding}, then the file
                contents will be processed using non-unicode byte
                strings.
              - B{A list}: C{encoding} should be a list of C{(regexp,
                encoding)} tuples.  The encoding for a file whose
                identifier is C{file_id} will be the C{encoding} value
                for the first tuple whose C{regexp} matches the
                C{file_id}.  If no tuple's C{regexp} matches the
                C{file_id}, the file contents will be processed using
                non-unicode byte strings.
              - C{None}: the file contents of all files will be
                processed using non-unicode byte strings.
        @param tag_mapping_function: A function for normalizing or
                simplifying the POS tags returned by the tagged_words()
                or tagged_sents() methods.
        """
        # Convert the root to a path pointer, if necessary.
        if isinstance(root, basestring):
            m = re.match('(.*\.zip)/?(.*)$|', root)
            zipfile, zipentry = m.groups()
            if zipfile:
                root = ZipFilePathPointer(zipfile, zipentry)
            else:
                root = FileSystemPathPointer(root)
        elif not isinstance(root, PathPointer):
            raise TypeError('CorpusReader: expected a string or a PathPointer')

        # If `fileids` is a regexp, then expand it.
        if isinstance(fileids, basestring):
            fileids = find_corpus_fileids(root, fileids)

        self._fileids = fileids
        """A list of the relative paths for the fileids that make up
        this corpus."""

        self._root = root
        """The root directory for this corpus."""

        # If encoding was specified as a list of regexps, then convert
        # it to a dictionary.
        if isinstance(encoding, list):
            encoding_dict = {}
            for fileid in self._fileids:
                for x in encoding:
                    (regexp, enc) = x
                    if re.match(regexp, fileid):
                        encoding_dict[fileid] = enc
                        break
            encoding = encoding_dict

        self._encoding = encoding
        """The default unicode encoding for the fileids that make up
           this corpus.  If C{encoding} is C{None}, then the file
           contents are processed using byte strings (C{str})."""
        self._tag_mapping_function = tag_mapping_function

    def __repr__(self):
        if isinstance(self._root, ZipFilePathPointer):
            path = '%s/%s' % (self._root.zipfile.filename, self._root.entry)
        else:
            path = '%s' % self._root.path
        return '<%s in %r>' % (self.__class__.__name__, path)

    def readme(self):
        """
        Return the contents of the corpus README file, if it exists.
        """

        return self.open("README").read()

    def fileids(self):
        """
        Return a list of file identifiers for the fileids that make up
        this corpus.
        """
        return self._fileids

    def abspath(self, fileid):
        """
        Return the absolute path for the given file.

        @type file: C{str}
        @param file: The file identifier for the file whose path
            should be returned.

        @rtype: L{PathPointer}
        """
        return self._root.join(fileid)

    def abspaths(self, fileids=None, include_encoding=False):
        """
        Return a list of the absolute paths for all fileids in this corpus;
        or for the given list of fileids, if specified.

        @type fileids: C{None} or C{str} or C{list}
        @param fileids: Specifies the set of fileids for which paths should
            be returned.  Can be C{None}, for all fileids; a list of
            file identifiers, for a specified set of fileids; or a single
            file identifier, for a single file.  Note that the return
            value is always a list of paths, even if C{fileids} is a
            single file identifier.

        @param include_encoding: If true, then return a list of
            C{(path_pointer, encoding)} tuples.

        @rtype: C{list} of L{PathPointer}
        """
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, basestring):
            fileids = [fileids]

        paths = [self._root.join(f) for f in fileids]

        if include_encoding:
            return zip(paths, [self.encoding(f) for f in fileids])
        else:
            return paths

    def open(self, file):
        """
        Return an open stream that can be used to read the given file.
        If the file's encoding is not C{None}, then the stream will
        automatically decode the file's contents into unicode.

        @param file: The file identifier of the file to read.
        """
        encoding = self.encoding(file)
        return self._root.join(file).open(encoding)

    def encoding(self, file):
        """
        Return the unicode encoding for the given corpus file, if known.
        If the encoding is unknown, or if the given file should be
        processed using byte strings (C{str}), then return C{None}.
        """
        if isinstance(self._encoding, dict):
            return self._encoding.get(file)
        else:
            return self._encoding

    def _get_root(self): return self._root
    root = property(_get_root, doc="""
        The directory where this corpus is stored.

        @type: L{PathPointer}""")

    #{ Deprecated since 0.9.7
    def files(self): return self.fileids()
    #}

    #{ Deprecated since 0.9.1
    def _get_items(self): return self.fileids()
    items = property(_get_items)
    #}

#=================================================================

# inherited from pywordnet, by Oliver Steele
def binary_search_file(file, key, cache={}, cacheDepth=-1):
    """
    Searches through a sorted file using the binary search algorithm.

    @type  file: file
    @param file: the file to be searched through.
    @type  key: {string}
    @param key: the identifier we are searching for.
    @return: The line from the file with first word key.
    """
    
    key = key + ' '
    keylen = len(key)
    start = 0
    currentDepth = 0

    if hasattr(file, 'name'):
        end = os.stat(file.name).st_size - 1
    else:
        file.seek(0, 2)
        end = file.tell() - 1
        file.seek(0)
        
    while start < end:
        lastState = start, end
        middle = (start + end) / 2

        if cache.get(middle):
            offset, line = cache[middle]

        else:
            line = ""
            while True:
                file.seek(max(0, middle - 1))
                if middle > 0:
                    file.readline()
                offset = file.tell()
                line = file.readline()
                if line != "": break
                # at EOF; try to find start of the last line
                middle = (start + middle)/2
                if middle == end -1:
                    return None
            if currentDepth < cacheDepth:
                cache[middle] = (offset, line)
                
        if offset > end:
            assert end != middle - 1, "infinite loop"
            end = middle - 1
        elif line[:keylen] == key:
            return line
        elif line > key:
            assert end != middle - 1, "infinite loop"
            end = middle - 1
        elif line < key:
            start = offset + len(line) - 1

        currentDepth += 1
        thisState = start, end

        if lastState == thisState:
            # Detects the condition where we're searching past the end
            # of the file, which is otherwise difficult to detect
            return None

    return None

#====================================================================

class FreqDist(dict):
    """
    A frequency distribution for the outcomes of an experiment.  A
    frequency distribution records the number of times each outcome of
    an experiment has occurred.  For example, a frequency distribution
    could be used to record the frequency of each word type in a
    document.  Formally, a frequency distribution can be defined as a
    function mapping from each sample to the number of times that
    sample occurred as an outcome.

    Frequency distributions are generally constructed by running a
    number of experiments, and incrementing the count for a sample
    every time it is an outcome of an experiment.  For example, the
    following code will produce a frequency distribution that encodes
    how often each word occurs in a text:

        >>> fdist = FreqDist()
        >>> for word in tokenize.whitespace(sent):
        ...    fdist.inc(word.lower())

    An equivalent way to do this is with the initializer:

        >>> fdist = FreqDist(word.lower() for word in tokenize.whitespace(sent))

    """
    def __init__(self, samples=None):
        """
        Construct a new frequency distribution.  If C{samples} is
        given, then the frequency distribution will be initialized
        with the count of each object in C{samples}; otherwise, it
        will be initialized to be empty.

        In particular, C{FreqDist()} returns an empty frequency
        distribution; and C{FreqDist(samples)} first creates an empty
        frequency distribution, and then calls C{update} with the 
        list C{samples}.

        @param samples: The samples to initialize the frequency
        distribution with.
        @type samples: Sequence
        """
        dict.__init__(self)
        self._N = 0
        self._Nr_cache = None
        self._max_cache = None
        self._item_cache = None
        if samples:
            self.update(samples)

    def inc(self, sample, count=1):
        """
        Increment this C{FreqDist}'s count for the given
        sample.

        @param sample: The sample whose count should be incremented.
        @type sample: any
        @param count: The amount to increment the sample's count by.
        @type count: C{int}
        @rtype: None
        @raise NotImplementedError: If C{sample} is not a
               supported sample type.
        """
        if count == 0: return
        self[sample] = self.get(sample,0) + count

    def __setitem__(self, sample, value):
        """
        Set this C{FreqDist}'s count for the given sample.

        @param sample: The sample whose count should be incremented.
        @type sample: any hashable object
        @param count: The new value for the sample's count
        @type count: C{int}
        @rtype: None
        @raise TypeError: If C{sample} is not a supported sample type.
        """

        self._N += (value - self.get(sample, 0))
        dict.__setitem__(self, sample, value)

        # Invalidate the Nr cache and max cache.
        self._Nr_cache = None
        self._max_cache = None
        self._item_cache = None

    def N(self):
        """
        @return: The total number of sample outcomes that have been
          recorded by this C{FreqDist}.  For the number of unique 
          sample values (or bins) with counts greater than zero, use
          C{FreqDist.B()}.
        @rtype: C{int}
        """
        return self._N

    def B(self):
        """
        @return: The total number of sample values (or X{bins}) that
            have counts greater than zero.  For the total
            number of sample outcomes recorded, use C{FreqDist.N()}.
            (FreqDist.B() is the same as len(FreqDist).)
        @rtype: C{int}
        """
        return len(self)

    # deprecate this -- use keys() instead?
    def samples(self):
        """
        @return: A list of all samples that have been recorded as
            outcomes by this frequency distribution.  Use C{count()}
            to determine the count for each sample.
        @rtype: C{list}
        """
        return self.keys()
    
    def hapaxes(self):
        """
        @return: A list of all samples that occur once (hapax legomena)
        @rtype: C{list}
        """
        return [item for item in self if self[item] == 1]

    def Nr(self, r, bins=None):
        """
        @return: The number of samples with count r.
        @rtype: C{int}
        @type r: C{int}
        @param r: A sample count.
        @type bins: C{int}
        @param bins: The number of possible sample outcomes.  C{bins}
            is used to calculate Nr(0).  In particular, Nr(0) is
            C{bins-self.B()}.  If C{bins} is not specified, it
            defaults to C{self.B()} (so Nr(0) will be 0).
        """
        if r < 0: raise IndexError, 'FreqDist.Nr(): r must be non-negative'

        # Special case for Nr(0):
        if r == 0:
            if bins is None: return 0
            else: return bins-self.B()

        # We have to search the entire distribution to find Nr.  Since
        # this is an expensive operation, and is likely to be used
        # repeatedly, cache the results.
        if self._Nr_cache is None:
            self._cache_Nr_values()

        if r >= len(self._Nr_cache): return 0
        return self._Nr_cache[r]

    def _cache_Nr_values(self):
        Nr = [0]
        for sample in self:
            c = self.get(sample, 0)
            if c >= len(Nr):
                Nr += [0]*(c+1-len(Nr))
            Nr[c] += 1
        self._Nr_cache = Nr

    def count(self, sample):
        """
        Return the count of a given sample.  The count of a sample is
        defined as the number of times that sample outcome was
        recorded by this C{FreqDist}.  Counts are non-negative
        integers.  This method has been replaced by conventional
        dictionary indexing; use fd[item] instead of fd.count(item).

        @return: The count of a given sample.
        @rtype: C{int}
        @param sample: the sample whose count
               should be returned.
        @type sample: any.
        """
        raise AttributeError, "Use indexing to look up an entry in a FreqDist, e.g. fd[item]"

    def _cumulative_frequencies(self, samples=None):
        """
        Return the cumulative frequencies of the specified samples.
        If no samples are specified, all counts are returned, starting
        with the largest.

        @return: The cumulative frequencies of the given samples.
        @rtype: C{list} of C{float}
        @param samples: the samples whose frequencies should be returned.
        @type sample: any.
        """
        cf = 0.0
        for sample in samples:
            cf += self[sample]
            yield cf
    
    # slightly odd nomenclature freq() if FreqDist does counts and ProbDist does probs,
    # here, freq() does probs
    def freq(self, sample):
        """
        Return the frequency of a given sample.  The frequency of a
        sample is defined as the count of that sample divided by the
        total number of sample outcomes that have been recorded by
        this C{FreqDist}.  The count of a sample is defined as the
        number of times that sample outcome was recorded by this
        C{FreqDist}.  Frequencies are always real numbers in the range
        [0, 1].

        @return: The frequency of a given sample.
        @rtype: float
        @param sample: the sample whose frequency
               should be returned.
        @type sample: any
        """
        if self._N is 0:
            return 0
        return float(self[sample]) / self._N

    def max(self):
        """
        Return the sample with the greatest number of outcomes in this
        frequency distribution.  If two or more samples have the same
        number of outcomes, return one of them; which sample is
        returned is undefined.  If no outcomes have occurred in this
        frequency distribution, return C{None}.

        @return: The sample with the maximum number of outcomes in this
                frequency distribution.
        @rtype: any or C{None}
        """
        if self._max_cache is None:
            best_sample = None
            best_count = -1
            for sample in self:
                if self[sample] > best_count:
                    best_sample = sample
                    best_count = self[sample]
            self._max_cache = best_sample
        return self._max_cache

    def plot(self, *args, **kwargs):
        """
        Plot samples from the frequency distribution
        displaying the most frequent sample first.  If an integer
        parameter is supplied, stop after this many samples have been
        plotted.  If two integer parameters m, n are supplied, plot a
        subset of the samples, beginning with m and stopping at n-1.
        For a cumulative plot, specify cumulative=True.
        (Requires Matplotlib to be installed.)

        @param title: The title for the graph
        @type title: C{str}
        @param cumulative: A flag to specify whether the plot is cumulative (default = False)
        @type title: C{bool}
        @param num: The maximum number of samples to plot (default=50).  Specify num=0 to get all samples (slow).
        @type num: C{int} 
        """
        try:
            import pylab
        except ImportError:
            raise ValueError('The plot function requires the matplotlib package.'
                         'See http://matplotlib.sourceforge.net/')
        
        if len(args) == 0:
            args = [len(self)]
        samples = list(islice(self, *args))
        
        cumulative = _get_kwarg(kwargs, 'cumulative', False)
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
            ylabel = "Cumulative Counts"
        else:
            freqs = [self[sample] for sample in samples]
            ylabel = "Counts"
        # percents = [f * 100 for f in freqs]  only in ProbDist?
        
        pylab.grid(True, color="silver")
        if not "linewidth" in kwargs:
            kwargs["linewidth"] = 2
        pylab.plot(freqs, **kwargs)
        pylab.xticks(range(len(samples)), [str(s) for s in samples], rotation=90)
        if "title" in kwargs: pylab.title(kwargs["title"])
        pylab.xlabel("Samples")
        pylab.ylabel(ylabel)
        pylab.show()
        
    def tabulate(self, *args, **kwargs):
        """
        Tabulate the given samples from the frequency distribution (cumulative),
        displaying the most frequent sample first.
        (Requires Matplotlib to be installed.)
        
        @param samples: The samples to plot (default is all samples)
        @type samples: C{list}
        @param title: The title for the graph
        @type title: C{str}
        @param num: The maximum number of samples to plot (default=50).  Specify num=0 to get all samples (slow).
        @type num: C{int} 
        """
        if len(args) == 0:
            args = [len(self)]
        samples = list(islice(self, *args))
        
        cumulative = _get_kwarg(kwargs, 'cumulative', False)
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
        else:
            freqs = [self[sample] for sample in samples]
        # percents = [f * 100 for f in freqs]  only in ProbDist?
        
        for i in range(len(samples)):
            print "%4s" % str(samples[i]),
        print
        for i in range(len(samples)):
            print "%4d" % freqs[i],
        print

    def sorted_samples(self):
        raise AttributeError, "Use FreqDist.keys(), or iterate over the FreqDist to get its samples in sorted order (most frequent first)"
    
    def sorted(self):
        raise AttributeError, "Use FreqDist.keys(), or iterate over the FreqDist to get its samples in sorted order (most frequent first)"
    
    def _sort_keys_by_value(self):
        if not self._item_cache:
            self._item_cache = sorted(dict.items(self), key=lambda x:(-x[1], x[0]))

    def keys(self):
        """
        Return the samples sorted in decreasing order of frequency.

        @return: A list of samples, in sorted order
        @rtype: C{list} of any
        """
        self._sort_keys_by_value()
        return map(itemgetter(0), self._item_cache)
    
    def values(self):
        """
        Return the samples sorted in decreasing order of frequency.

        @return: A list of samples, in sorted order
        @rtype: C{list} of any
        """
        self._sort_keys_by_value()
        return map(itemgetter(1), self._item_cache)
    
    def items(self):
        """
        Return the items sorted in decreasing order of frequency.

        @return: A list of items, in sorted order
        @rtype: C{list} of C{tuple}
        """
        self._sort_keys_by_value()
        return self._item_cache[:]
    
    def __iter__(self):
        """
        Return the samples sorted in decreasing order of frequency.

        @return: An iterator over the samples, in sorted order
        @rtype: C{iter}
        """
        return iter(self.keys())

    def iterkeys(self):
        """
        Return the samples sorted in decreasing order of frequency.

        @return: An iterator over the samples, in sorted order
        @rtype: C{iter}
        """
        return iter(self.keys())

    def itervalues(self):
        """
        Return the values sorted in decreasing order.

        @return: An iterator over the values, in sorted order
        @rtype: C{iter}
        """
        return iter(self.values())

    def iteritems(self):
        """
        Return the items sorted in decreasing order of frequency.

        @return: An iterator over the items, in sorted order
        @rtype: C{iter} of any
        """
        self._sort_keys_by_value()
        return iter(self._item_cache)

#        sort the supplied samples
#        if samples:
#            items = [(sample, self[sample]) for sample in set(samples)]

    def copy(self):
        """
        Create a copy of this frequency distribution.
        
        @return: A copy of this frequency distribution object.
        @rtype: C{FreqDist}
        """
        return self.__class__(self)
    
    def update(self, samples):
        """
        Update the frequency distribution with the provided list of samples.
        This is a faster way to add multiple samples to the distribution.
        
        @param samples: The samples to add.
        @type samples: C{list}
        """
        try:
            sample_iter = samples.iteritems()
        except:
            sample_iter = imap(lambda x: (x,1), samples)
        for sample, count in sample_iter:
            self.inc(sample, count=count)    
    
    def __add__(self, other):
        clone = self.copy()
        clone.update(other)
        return clone
    def __eq__(self, other):
        if not isinstance(other, FreqDist): return False
        return self.items() == other.items() # items are already sorted
    def __ne__(self, other):
        return not (self == other)
    def __le__(self, other):
        if not isinstance(other, FreqDist): return False
        return set(self).issubset(other) and all(self[key] <= other[key] for key in self)
    def __lt__(self, other):
        if not isinstance(other, FreqDist): return False
        return self <= other and self != other
    def __ge__(self, other):
        if not isinstance(other, FreqDist): return False
        return other <= self
    def __gt__(self, other):
        if not isinstance(other, FreqDist): return False
        return other < self
    
    def __repr__(self):
        """
        @return: A string representation of this C{FreqDist}.
        @rtype: string
        """
        return '<FreqDist with %d outcomes>' % self.N()

    def __str__(self):
        """
        @return: A string representation of this C{FreqDist}.
        @rtype: string
        """
        items = ['%r: %r' % (s, self[s]) for s in self]
        return '<FreqDist: %s>' % ', '.join(items)

    def __getitem__(self, sample):
        return self.get(sample, 0)

