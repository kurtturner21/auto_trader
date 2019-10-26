Microsoft Windows [Version 10.0.18362.418]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\kturner>cd \dev\auto_trader\apps

C:\dev\auto_trader\apps>python
Python 3.5.3 (v3.5.3:1880cb95a742, Jan 16 2017, 16:02:32) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import auto_trader as at
>>> date_start = at.datetime(2000 + y_int, m_int+1, 1, 0, 0, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'y_int' is not defined
>>> date_start = at.datetime(2000 + 1, 1+1, 1, 0, 0, 0)
>>> date_start
datetime.datetime(2001, 2, 1, 0, 0)
>>> yyyy_mm_code = at.datetime.strftime(date_start, '%Y_%m')
>>> yyyy_mm_code
'2001_02'
>>> yr_mth_fpath = at.define_monthly_frames_history_path(yyyy_mm_code)
>>> mth = at.d.read_csv(yr_mth_fpath)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'auto_trader' has no attribute 'd'
>>> mth = at.pd.read_csv(yr_mth_fpath)
>>> mth
           Date    sk   100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open    Volume    nma   pct  sk.1
0    2001-02-01   cuz  24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020   20100.0  75.75 -0.04   cuz
1    2001-02-02   cuz  24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048   14300.0  75.65 -0.05   cuz
2    2001-02-05   cuz  24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500   46600.0  75.68 -0.03   cuz
3    2001-02-06   cuz  24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370  151100.0  75.45 -0.04   cuz
4    2001-02-07   cuz  24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677   18200.0  75.17 -0.01   cuz
..          ...   ...     ...     ...     ...        ...     ...     ...     ...     ...     ...       ...    ...   ...   ...
584  2001-02-22  ssys   1.212   1.708   1.055      1.000   1.000     NaN   1.052   0.958   1.010   84000.0   1.01  0.12  ssys
585  2001-02-23  ssys   1.204   1.702   1.059      1.021   1.021     NaN   1.062   1.000   1.000   22200.0   1.01  0.11  ssys
586  2001-02-26  ssys   1.197   1.696   1.058      1.052   1.052     NaN   1.062   1.021   1.021    4400.0   1.02 -0.03  ssys
587  2001-02-27  ssys   1.189   1.690   1.057      1.031   1.031     NaN   1.062   1.031   1.042   32400.0   1.02 -0.01  ssys
588  2001-02-28  ssys   1.183   1.683   1.055      1.021   1.021     NaN   1.036   1.021   1.036    5000.0   1.02 -0.06  ssys

[589 rows x 15 columns]
>>> mth = at.pd.read_csv(yr_mth_fpath, parse_dates=True, index_col=0,1)
  File "<stdin>", line 1
SyntaxError: positional argument follows keyword argument
>>> mth = at.pd.read_csv(yr_mth_fpath, parse_dates=True, index_col=[0,1])
>>> mth
                  100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open    Volume    nma   pct  sk.1
Date       sk
2001-02-01 cuz   24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020   20100.0  75.75 -0.04   cuz
2001-02-02 cuz   24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048   14300.0  75.65 -0.05   cuz
2001-02-05 cuz   24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500   46600.0  75.68 -0.03   cuz
2001-02-06 cuz   24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370  151100.0  75.45 -0.04   cuz
2001-02-07 cuz   24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677   18200.0  75.17 -0.01   cuz
...                 ...     ...     ...        ...     ...     ...     ...     ...     ...       ...    ...   ...   ...
2001-02-22 ssys   1.212   1.708   1.055      1.000   1.000     NaN   1.052   0.958   1.010   84000.0   1.01  0.12  ssys
2001-02-23 ssys   1.204   1.702   1.059      1.021   1.021     NaN   1.062   1.000   1.000   22200.0   1.01  0.11  ssys
2001-02-26 ssys   1.197   1.696   1.058      1.052   1.052     NaN   1.062   1.021   1.021    4400.0   1.02 -0.03  ssys
2001-02-27 ssys   1.189   1.690   1.057      1.031   1.031     NaN   1.062   1.031   1.042   32400.0   1.02 -0.01  ssys
2001-02-28 ssys   1.183   1.683   1.055      1.021   1.021     NaN   1.036   1.021   1.036    5000.0   1.02 -0.06  ssys

[589 rows x 13 columns]
>>> mth
                  100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open    Volume    nma   pct  sk.1
Date       sk
2001-02-01 cuz   24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020   20100.0  75.75 -0.04   cuz
2001-02-02 cuz   24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048   14300.0  75.65 -0.05   cuz
2001-02-05 cuz   24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500   46600.0  75.68 -0.03   cuz
2001-02-06 cuz   24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370  151100.0  75.45 -0.04   cuz
2001-02-07 cuz   24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677   18200.0  75.17 -0.01   cuz
...                 ...     ...     ...        ...     ...     ...     ...     ...     ...       ...    ...   ...   ...
2001-02-22 ssys   1.212   1.708   1.055      1.000   1.000     NaN   1.052   0.958   1.010   84000.0   1.01  0.12  ssys
2001-02-23 ssys   1.204   1.702   1.059      1.021   1.021     NaN   1.062   1.000   1.000   22200.0   1.01  0.11  ssys
2001-02-26 ssys   1.197   1.696   1.058      1.052   1.052     NaN   1.062   1.021   1.021    4400.0   1.02 -0.03  ssys
2001-02-27 ssys   1.189   1.690   1.057      1.031   1.031     NaN   1.062   1.031   1.042   32400.0   1.02 -0.01  ssys
2001-02-28 ssys   1.183   1.683   1.055      1.021   1.021     NaN   1.036   1.021   1.036    5000.0   1.02 -0.06  ssys

[589 rows x 13 columns]
>>> mth[at.datetime(2001, 2, 1, 6, 0, 0):]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\frame.py", line 2961, in __getitem__
    indexer = convert_to_index_sliceable(self, key)
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 2358, in convert_to_index_sliceable
    return idx._convert_slice_indexer(key, kind="getitem")
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 3216, in _convert_slice_indexer
    indexer = self.slice_indexer(start, stop, step, kind=kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 5034, in slice_indexer
    start_slice, end_slice = self.slice_locs(start, end, step=step, kind=kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2581, in slice_locs
    return super().slice_locs(start, end, step, kind=kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 5248, in slice_locs
    start_slice = self.get_slice_bound(start, "left", kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2525, in get_slice_bound
    return self._partial_tup_index(label, side=side)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2587, in _partial_tup_index
    " lexsort depth (%d)" % (len(tup), self.lexsort_depth)
pandas.errors.UnsortedIndexError: 'Key length (1) was greater than MultiIndex lexsort depth (0)'
>>> mth.loc[at.datetime(2001, 2, 1, 6, 0, 0):]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 1424, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 1797, in _getitem_axis
    return self._get_slice_axis(key, axis=axis)
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 1454, in _get_slice_axis
    slice_obj.start, slice_obj.stop, slice_obj.step, kind=self.name
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 5034, in slice_indexer
    start_slice, end_slice = self.slice_locs(start, end, step=step, kind=kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2581, in slice_locs
    return super().slice_locs(start, end, step, kind=kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 5248, in slice_locs
    start_slice = self.get_slice_bound(start, "left", kind)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2525, in get_slice_bound
    return self._partial_tup_index(label, side=side)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2587, in _partial_tup_index
    " lexsort depth (%d)" % (len(tup), self.lexsort_depth)
pandas.errors.UnsortedIndexError: 'Key length (1) was greater than MultiIndex lexsort depth (0)'
>>> mth.loc[at.datetime(2001, 2, 1, 6, 0, 0):*]
  File "<stdin>", line 1
    mth.loc[at.datetime(2001, 2, 1, 6, 0, 0):*]
                                             ^
SyntaxError: invalid syntax
>>> mth.loc[at.datetime(2001, 2, 1, 6, 0, 0)]
Traceback (most recent call last):
  File "pandas\_libs\index.pyx", line 438, in pandas._libs.index.DatetimeEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 992, in pandas._libs.hashtable.Int64HashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 998, in pandas._libs.hashtable.Int64HashTable.get_item
KeyError: 981007200000000000

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2897, in get_loc
    return self._engine.get_loc(key)
  File "pandas\_libs\index.pyx", line 410, in pandas._libs.index.DatetimeEngine.get_loc
  File "pandas\_libs\index.pyx", line 440, in pandas._libs.index.DatetimeEngine.get_loc
KeyError: Timestamp('2001-02-01 06:00:00')

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "pandas\_libs\index.pyx", line 438, in pandas._libs.index.DatetimeEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 992, in pandas._libs.hashtable.Int64HashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 998, in pandas._libs.hashtable.Int64HashTable.get_item
KeyError: 981007200000000000

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 1424, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 1850, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "C:\Python35\lib\site-packages\pandas\core\indexing.py", line 160, in _get_label
    return self.obj._xs(label, axis=axis)
  File "C:\Python35\lib\site-packages\pandas\core\generic.py", line 3735, in xs
    loc, new_index = self.index.get_loc_level(key, drop_level=drop_level)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2856, in get_loc_level
    indexer = self._get_level_indexer(key, level=level)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 2939, in _get_level_indexer
    code = level_index.get_loc(key)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\datetimes.py", line 1039, in get_loc
    return Index.get_loc(self, key, method, tolerance)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2899, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas\_libs\index.pyx", line 410, in pandas._libs.index.DatetimeEngine.get_loc
  File "pandas\_libs\index.pyx", line 440, in pandas._libs.index.DatetimeEngine.get_loc
KeyError: Timestamp('2001-02-01 06:00:00')
>>> mth[mth.index.isin(at.datetime(2001, 2, 1, 6, 0, 0)]
  File "<stdin>", line 1
    mth[mth.index.isin(at.datetime(2001, 2, 1, 6, 0, 0)]
                                                       ^
SyntaxError: invalid syntax
>>> mth[mth.index.isin(at.datetime(2001, 2, 1, 6, 0, 0))]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 3426, in isin
    values = MultiIndex.from_tuples(values, names=self.names).values
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 470, in from_tuples
    raise TypeError("Input must be a list / sequence of tuple-likes.")
TypeError: Input must be a list / sequence of tuple-likes.
>>> mth
                  100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open    Volume    nma   pct  sk.1
Date       sk
2001-02-01 cuz   24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020   20100.0  75.75 -0.04   cuz
2001-02-02 cuz   24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048   14300.0  75.65 -0.05   cuz
2001-02-05 cuz   24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500   46600.0  75.68 -0.03   cuz
2001-02-06 cuz   24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370  151100.0  75.45 -0.04   cuz
2001-02-07 cuz   24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677   18200.0  75.17 -0.01   cuz
...                 ...     ...     ...        ...     ...     ...     ...     ...     ...       ...    ...   ...   ...
2001-02-22 ssys   1.212   1.708   1.055      1.000   1.000     NaN   1.052   0.958   1.010   84000.0   1.01  0.12  ssys
2001-02-23 ssys   1.204   1.702   1.059      1.021   1.021     NaN   1.062   1.000   1.000   22200.0   1.01  0.11  ssys
2001-02-26 ssys   1.197   1.696   1.058      1.052   1.052     NaN   1.062   1.021   1.021    4400.0   1.02 -0.03  ssys
2001-02-27 ssys   1.189   1.690   1.057      1.031   1.031     NaN   1.062   1.031   1.042   32400.0   1.02 -0.01  ssys
2001-02-28 ssys   1.183   1.683   1.055      1.021   1.021     NaN   1.036   1.021   1.036    5000.0   1.02 -0.06  ssys

[589 rows x 13 columns]
>>> mth.filter(like='s')
                 Adj Close   Close  sk.1
Date       sk
2001-02-01 cuz      24.567  76.048   cuz
2001-02-02 cuz      24.120  74.665   cuz
2001-02-05 cuz      24.348  75.370   cuz
2001-02-06 cuz      24.166  74.806   cuz
2001-02-07 cuz      24.526  74.947   cuz
...                    ...     ...   ...
2001-02-22 ssys      1.000   1.000  ssys
2001-02-23 ssys      1.021   1.021  ssys
2001-02-26 ssys      1.052   1.052  ssys
2001-02-27 ssys      1.031   1.031  ssys
2001-02-28 ssys      1.021   1.021  ssys

[589 rows x 3 columns]
>>> mth.filter(like='s', axis=2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\generic.py", line 4655, in filter
    labels = self._get_axis(axis)
  File "C:\Python35\lib\site-packages\pandas\core\generic.py", line 427, in _get_axis
    name = self._get_axis_name(axis)
  File "C:\Python35\lib\site-packages\pandas\core\generic.py", line 424, in _get_axis_name
    raise ValueError("No axis named {0} for object type {1}".format(axis, cls))
ValueError: No axis named 2 for object type <class 'pandas.core.frame.DataFrame'>
>>> mth.filter(like='s', axis=1)
                 Adj Close   Close  sk.1
Date       sk
2001-02-01 cuz      24.567  76.048   cuz
2001-02-02 cuz      24.120  74.665   cuz
2001-02-05 cuz      24.348  75.370   cuz
2001-02-06 cuz      24.166  74.806   cuz
2001-02-07 cuz      24.526  74.947   cuz
...                    ...     ...   ...
2001-02-22 ssys      1.000   1.000  ssys
2001-02-23 ssys      1.021   1.021  ssys
2001-02-26 ssys      1.052   1.052  ssys
2001-02-27 ssys      1.031   1.031  ssys
2001-02-28 ssys      1.021   1.021  ssys

[589 rows x 3 columns]
>>> mth.filter(like='ss', axis=1)
Empty DataFrame
Columns: []
Index: [(2001-02-01 00:00:00, cuz), (2001-02-02 00:00:00, cuz), (2001-02-05 00:00:00, cuz), (2001-02-06 00:00:00, cuz), (2001-02-07 00:00:00, cuz), (2001-02-08 00:00:00, cuz), (2001-02-09 00:00:00, cuz), (2001-02-12 00:00:00, cuz), (2001-02-13 00:00:00, cuz), (2001-02-14 00:00:00, cuz), (2001-02-15 00:00:00, cuz), (2001-02-16 00:00:00, cuz), (2001-02-20 00:00:00, cuz), (2001-02-21 00:00:00, cuz), (2001-02-22 00:00:00, cuz), (2001-02-23 00:00:00, cuz), (2001-02-26 00:00:00, cuz), (2001-02-27 00:00:00, cuz), (2001-02-28 00:00:00, cuz), (2001-02-01 00:00:00, ug), (2001-02-02 00:00:00, ug), (2001-02-05 00:00:00, ug), (2001-02-06 00:00:00, ug), (2001-02-07 00:00:00, ug), (2001-02-08 00:00:00, ug), (2001-02-09 00:00:00, ug), (2001-02-12 00:00:00, ug), (2001-02-13 00:00:00, ug), (2001-02-14 00:00:00, ug), (2001-02-15 00:00:00, ug), (2001-02-16 00:00:00, ug), (2001-02-20 00:00:00, ug), (2001-02-21 00:00:00, ug), (2001-02-22 00:00:00, ug), (2001-02-23 00:00:00, ug), (2001-02-26 00:00:00, ug), (2001-02-27 00:00:00, ug), (2001-02-28 00:00:00, ug), (2001-02-01 00:00:00, trns), (2001-02-02 00:00:00, trns), (2001-02-05 00:00:00, trns), (2001-02-06 00:00:00, trns), (2001-02-07 00:00:00, trns), (2001-02-08 00:00:00, trns), (2001-02-09 00:00:00, trns), (2001-02-12 00:00:00, trns), (2001-02-13 00:00:00, trns), (2001-02-14 00:00:00, trns), (2001-02-15 00:00:00, trns), (2001-02-16 00:00:00, trns), (2001-02-20 00:00:00, trns), (2001-02-21 00:00:00, trns), (2001-02-22 00:00:00, trns), (2001-02-23 00:00:00, trns), (2001-02-26 00:00:00, trns), (2001-02-27 00:00:00, trns), (2001-02-28 00:00:00, trns), (2001-02-01 00:00:00, alg), (2001-02-02 00:00:00, alg), (2001-02-05 00:00:00, alg), (2001-02-06 00:00:00, alg), (2001-02-07 00:00:00, alg), (2001-02-08 00:00:00, alg), (2001-02-09 00:00:00, alg), (2001-02-12 00:00:00, alg), (2001-02-13 00:00:00, alg), (2001-02-14 00:00:00, alg), (2001-02-15 00:00:00, alg), (2001-02-16 00:00:00, alg), (2001-02-20 00:00:00, alg), (2001-02-21 00:00:00, alg), (2001-02-22 00:00:00, alg), (2001-02-23 00:00:00, alg), (2001-02-26 00:00:00, alg), (2001-02-27 00:00:00, alg), (2001-02-28 00:00:00, alg), (2001-02-01 00:00:00, bios), (2001-02-02 00:00:00, bios), (2001-02-05 00:00:00, bios), (2001-02-06 00:00:00, bios), (2001-02-07 00:00:00, bios), (2001-02-08 00:00:00, bios), (2001-02-09 00:00:00, bios), (2001-02-12 00:00:00, bios), (2001-02-13 00:00:00, bios), (2001-02-14 00:00:00, bios), (2001-02-15 00:00:00, bios), (2001-02-16 00:00:00, bios), (2001-02-20 00:00:00, bios), (2001-02-21 00:00:00, bios), (2001-02-22 00:00:00, bios), (2001-02-23 00:00:00, bios), (2001-02-26 00:00:00, bios), (2001-02-27 00:00:00, bios), (2001-02-28 00:00:00, bios), (2001-02-01 00:00:00, ewh), (2001-02-02 00:00:00, ewh), (2001-02-05 00:00:00, ewh), (2001-02-06 00:00:00, ewh), (2001-02-07 00:00:00, ewh), ...]

[589 rows x 0 columns]
>>> mth.filter(like='s')
                 Adj Close   Close  sk.1
Date       sk
2001-02-01 cuz      24.567  76.048   cuz
2001-02-02 cuz      24.120  74.665   cuz
2001-02-05 cuz      24.348  75.370   cuz
2001-02-06 cuz      24.166  74.806   cuz
2001-02-07 cuz      24.526  74.947   cuz
...                    ...     ...   ...
2001-02-22 ssys      1.000   1.000  ssys
2001-02-23 ssys      1.021   1.021  ssys
2001-02-26 ssys      1.052   1.052  ssys
2001-02-27 ssys      1.031   1.031  ssys
2001-02-28 ssys      1.021   1.021  ssys

[589 rows x 3 columns]
>>> mth.filter(index=['sk'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: filter() got an unexpected keyword argument 'index'
>>> dir(mth)
['Close', 'High', 'Low', 'Open', 'T', 'Volume', '_AXIS_ALIASES', '_AXIS_IALIASES', '_AXIS_LEN', '_AXIS_NAMES', '_AXIS_NUMBERS', '_AXIS_ORDERS', '_AXIS_REVERSED', '__abs__', '__add__', '__and__', '__array__', '__array_priority__', '__array_wrap__', '__bool__', '__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__div__', '__doc__', '__eq__', '__finalize__', '__floordiv__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__iand__', '__ifloordiv__', '__imod__', '__imul__', '__init__', '__invert__', '__ior__', '__ipow__', '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', '__lt__', '__matmul__', '__mod__', '__module__', '__mul__', '__ne__', '__neg__', '__new__', '__nonzero__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdiv__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rmatmul__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__setitem__', '__setstate__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__weakref__', '__xor__', '_accessors', '_add_numeric_operations', '_add_series_only_operations', '_add_series_or_dataframe_operations', '_agg_by_level', '_agg_examples_doc', '_agg_summary_and_see_also_doc', '_aggregate', '_aggregate_multiple_funcs', '_align_frame', '_align_series', '_box_col_values', '_box_item_values', '_builtin_table', '_check_inplace_setting', '_check_is_chained_assignment_possible', '_check_label_or_level_ambiguity', '_check_percentile', '_check_setitem_copy', '_clear_item_cache', '_clip_with_one_bound', '_clip_with_scalar', '_combine_const', '_combine_frame', '_combine_match_columns', '_combine_match_index', '_consolidate', '_consolidate_inplace', '_construct_axes_dict', '_construct_axes_dict_from', '_construct_axes_from_arguments', '_constructor', '_constructor_expanddim', '_constructor_sliced', '_convert', '_count_level', '_create_indexer', '_cython_table', '_data', '_deprecations', '_dir_additions', '_dir_deletions', '_drop_axis', '_drop_labels_or_levels', '_ensure_valid_index', '_find_valid_index', '_from_arrays', '_from_axes', '_get_agg_axis', '_get_axis', '_get_axis_name', '_get_axis_number', '_get_axis_resolvers', '_get_block_manager_axis', '_get_bool_data', '_get_cacher', '_get_index_resolvers', '_get_item_cache', '_get_label_or_level_values', '_get_numeric_data', '_get_space_character_free_column_resolvers', '_get_value', '_get_values', '_getitem_bool_array', '_getitem_frame', '_getitem_multilevel', '_gotitem', '_iget_item_cache', '_indexed_same', '_info_axis', '_info_axis_name', '_info_axis_number', '_info_repr', '_init_mgr', '_internal_get_values', '_internal_names', '_internal_names_set', '_is_builtin_func', '_is_cached', '_is_copy', '_is_cython_func', '_is_datelike_mixed_type', '_is_homogeneous_type', '_is_label_or_level_reference', '_is_label_reference', '_is_level_reference', '_is_mixed_type', '_is_numeric_mixed_type', '_is_view', '_ix', '_ixs', '_join_compat', '_maybe_cache_changed', '_maybe_update_cacher', '_metadata', '_needs_reindex_multi', '_obj_with_exclusions', '_protect_consolidate', '_reduce', '_reindex_axes', '_reindex_columns', '_reindex_index', '_reindex_multi', '_reindex_with_indexers', '_repr_data_resource_', '_repr_fits_horizontal_', '_repr_fits_vertical_', '_repr_html_', '_repr_latex_', '_reset_cache', '_reset_cacher', '_sanitize_column', '_selected_obj', '_selection', '_selection_list', '_selection_name', '_series', '_set_as_cached', '_set_axis', '_set_axis_name', '_set_is_copy', '_set_item', '_set_value', '_setitem_array', '_setitem_frame', '_setitem_slice', '_setup_axes', '_shallow_copy', '_slice', '_stat_axis', '_stat_axis_name', '_stat_axis_number', '_to_dict_of_blocks', '_try_aggregate_string_function', '_typ', '_unpickle_frame_compat', '_unpickle_matrix_compat', '_update_inplace', '_validate_dtype', '_values', '_where', '_xs', 'abs', 'add', 'add_prefix', 'add_suffix', 'agg', 'aggregate', 'align', 'all', 'any', 'append', 'apply', 'applymap', 'as_matrix', 'asfreq', 'asof', 'assign', 'astype', 'at', 'at_time', 'axes', 'between_time', 'bfill', 'bool', 'boxplot', 'clip', 'clip_lower', 'clip_upper', 'columns', 'combine', 'combine_first', 'compound', 'copy', 'corr', 'corrwith', 'count', 'cov', 'cummax', 'cummin', 'cumprod', 'cumsum', 'describe', 'diff', 'div', 'divide', 'dot', 'drop', 'drop_duplicates', 'droplevel', 'dropna', 'dtypes', 'duplicated', 'empty', 'eq', 'equals', 'eval', 'ewm', 'expanding', 'explode', 'ffill', 'fillna', 'filter', 'first', 'first_valid_index', 'floordiv', 'from_dict', 'from_records', 'ftypes', 'ge', 'get', 'get_dtype_counts', 'get_ftype_counts', 'get_values', 'groupby', 'gt', 'head', 'hist', 'iat', 'idxmax', 'idxmin', 'iloc', 'index', 'infer_objects', 'info', 'insert', 'interpolate', 'isin', 'isna', 'isnull', 'items', 'iteritems', 'iterrows', 'itertuples', 'ix', 'join', 'keys', 'kurt', 'kurtosis', 'last', 'last_valid_index', 'le', 'loc', 'lookup', 'lt', 'mad', 'mask', 'max', 'mean', 'median', 'melt', 'memory_usage', 'merge', 'min', 'mod', 'mode', 'mul', 'multiply', 'ndim', 'ne', 'nlargest', 'nma', 'notna', 'notnull', 'nsmallest', 'nunique', 'pct', 'pct_change', 'pipe', 'pivot', 'pivot_table', 'plot', 'pop', 'pow', 'prod', 'product', 'quantile', 'query', 'radd', 'rank', 'rdiv', 'reindex', 'reindex_like', 'rename', 'rename_axis', 'reorder_levels', 'replace', 'resample', 'reset_index', 'rfloordiv', 'rmod', 'rmul', 'rolling', 'round', 'rpow', 'rsub', 'rtruediv', 'sample', 'select_dtypes', 'sem', 'set_axis', 'set_index', 'shape', 'shift', 'size', 'skew', 'slice_shift', 'sort_index', 'sort_values', 'sparse', 'squeeze', 'stack', 'std', 'style', 'sub', 'subtract', 'sum', 'swapaxes', 'swaplevel', 'tail', 'take', 'to_clipboard', 'to_csv', 'to_dense', 'to_dict', 'to_excel', 'to_feather', 'to_gbq', 'to_hdf', 'to_html', 'to_json', 'to_latex', 'to_msgpack', 'to_numpy', 'to_parquet', 'to_period', 'to_pickle', 'to_records', 'to_sparse', 'to_sql', 'to_stata', 'to_string', 'to_timestamp', 'to_xarray', 'transform', 'transpose', 'truediv', 'truncate', 'tshift', 'tz_convert', 'tz_localize', 'unstack', 'update', 'values', 'var', 'where', 'xs']
>>> mth.index['Date'] < '2001-06-01'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 1996, in __getitem__
    if level_codes[key] == -1:
IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
>>> mth.loc[mth.index['Date'] < (at.datetime(2001, 2, 1, 6, 0, 0)]
  File "<stdin>", line 1
    mth.loc[mth.index['Date'] < (at.datetime(2001, 2, 1, 6, 0, 0)]
                                                                 ^
SyntaxError: invalid syntax
>>> mth.loc[mth.index['Date'] < at.datetime(2001, 2, 1, 6, 0, 0)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 1996, in __getitem__
    if level_codes[key] == -1:
IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
>>> mth.index['Date'] < at.datetime(2001, 2, 1, 6, 0, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 1996, in __getitem__
    if level_codes[key] == -1:
IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
>>> mth.index[0] < at.datetime(2001, 2, 1, 6, 0, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unorderable types: tuple() < datetime.datetime()
>>> mth.index < at.datetime(2001, 2, 1, 6, 0, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 111, in cmp_method
    result = op(self.values, np.asarray(other))
TypeError: unorderable types: tuple() < datetime.datetime()
>>> mth.index['sk']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\indexes\multi.py", line 1996, in __getitem__
    if level_codes[key] == -1:
IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
>>> mth[at.datetime(2001, 2, 1, 6, 0, 0).]
  File "<stdin>", line 1
    mth[at.datetime(2001, 2, 1, 6, 0, 0).]
                                         ^
SyntaxError: invalid syntax
>>> mth[at.datetime(2001, 2, 1, 6, 0, 0),]
Traceback (most recent call last):
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2897, in get_loc
    return self._engine.get_loc(key)
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: (datetime.datetime(2001, 2, 1, 6, 0),)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\frame.py", line 2980, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2899, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: (datetime.datetime(2001, 2, 1, 6, 0),)
>>> mth[[at.datetime(2001, 2, 1, 6, 0, 0)],]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\frame.py", line 2980, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2897, in get_loc
    return self._engine.get_loc(key)
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 109, in pandas._libs.index.IndexEngine.get_loc
TypeError: '([datetime.datetime(2001, 2, 1, 6, 0)],)' is an invalid key
>>> mth[[str(at.datetime(2001, 2, 1, 6, 0, 0)]),]
  File "<stdin>", line 1
    mth[[str(at.datetime(2001, 2, 1, 6, 0, 0)]),]
                                             ^
SyntaxError: invalid syntax
>>> mth
                  100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open    Volume    nma   pct  sk.1
Date       sk
2001-02-01 cuz   24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020   20100.0  75.75 -0.04   cuz
2001-02-02 cuz   24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048   14300.0  75.65 -0.05   cuz
2001-02-05 cuz   24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500   46600.0  75.68 -0.03   cuz
2001-02-06 cuz   24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370  151100.0  75.45 -0.04   cuz
2001-02-07 cuz   24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677   18200.0  75.17 -0.01   cuz
...                 ...     ...     ...        ...     ...     ...     ...     ...     ...       ...    ...   ...   ...
2001-02-22 ssys   1.212   1.708   1.055      1.000   1.000     NaN   1.052   0.958   1.010   84000.0   1.01  0.12  ssys
2001-02-23 ssys   1.204   1.702   1.059      1.021   1.021     NaN   1.062   1.000   1.000   22200.0   1.01  0.11  ssys
2001-02-26 ssys   1.197   1.696   1.058      1.052   1.052     NaN   1.062   1.021   1.021    4400.0   1.02 -0.03  ssys
2001-02-27 ssys   1.189   1.690   1.057      1.031   1.031     NaN   1.062   1.031   1.042   32400.0   1.02 -0.01  ssys
2001-02-28 ssys   1.183   1.683   1.055      1.021   1.021     NaN   1.036   1.021   1.036    5000.0   1.02 -0.06  ssys

[589 rows x 13 columns]
>>> mth['2001-02-06',]
Traceback (most recent call last):
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2897, in get_loc
    return self._engine.get_loc(key)
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: ('2001-02-06',)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\frame.py", line 2980, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2899, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: ('2001-02-06',)
>>> mth[5,]
Traceback (most recent call last):
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2897, in get_loc
    return self._engine.get_loc(key)
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: (5,)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python35\lib\site-packages\pandas\core\frame.py", line 2980, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Python35\lib\site-packages\pandas\core\indexes\base.py", line 2899, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas\_libs\index.pyx", line 107, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\index.pyx", line 131, in pandas._libs.index.IndexEngine.get_loc
  File "pandas\_libs\hashtable_class_helper.pxi", line 1607, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas\_libs\hashtable_class_helper.pxi", line 1614, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: (5,)
>>> mth.iloc[mth.index.get_level_values('sk') == 'cuz']
                 100ma   200ma    30ma  Adj Close   Close  Date.1    High     Low    Open     Volume    nma   pct sk.1
Date       sk
2001-02-01 cuz  24.703  24.370  24.633     24.567  76.048     NaN  76.048  75.342  76.020    20100.0  75.75 -0.04  cuz
2001-02-02 cuz  24.683  24.376  24.589     24.120  74.665     NaN  76.189  74.665  76.048    14300.0  75.65 -0.05  cuz
2001-02-05 cuz  24.664  24.382  24.561     24.348  75.370     NaN  77.488  75.229  76.500    46600.0  75.68 -0.03  cuz
2001-02-06 cuz  24.646  24.385  24.525     24.166  74.806     NaN  75.370  69.330  75.370   151100.0  75.45 -0.04  cuz
2001-02-07 cuz  24.630  24.392  24.526     24.526  74.947     NaN  75.229  73.423  73.677    18200.0  75.17 -0.01  cuz
2001-02-08 cuz  24.612  24.397  24.505     24.157  73.818     NaN  74.947  73.394  74.947    31200.0  74.72 -0.04  cuz
2001-02-09 cuz  24.599  24.403  24.481     24.489  74.834     NaN  74.834  73.677  73.987  2143100.0  74.75 -0.04  cuz
2001-02-12 cuz  24.579  24.409  24.446     24.360  74.439     NaN  74.806  73.592  74.806    12000.0  74.57 -0.05  cuz
2001-02-13 cuz  24.559  24.414  24.400     24.101  73.649     NaN  74.693  73.507  74.411    24300.0  74.34 -0.07  cuz
2001-02-14 cuz  24.542  24.419  24.364     24.009  73.366     NaN  73.677  73.112  73.649    66500.0  74.02 -0.05  cuz
2001-02-15 cuz  24.516  24.422  24.297     23.510  71.842     NaN  73.366  71.842  73.366    18900.0  73.63 -0.09  cuz
2001-02-16 cuz  24.493  24.426  24.244     23.602  72.124     NaN  72.830  71.221  71.842    65200.0  73.08 -0.08  cuz
2001-02-20 cuz  24.468  24.430  24.204     23.667  72.322     NaN  72.717  70.797  72.548    62300.0  72.66 -0.06  cuz
2001-02-21 cuz  24.442  24.433  24.175     23.695  72.406     NaN  72.632  71.616  71.616    54300.0  72.41 -0.05  cuz
2001-02-22 cuz  24.414  24.435  24.140     23.288  71.164     NaN  72.406  70.628  72.406    65000.0  71.97 -0.06  cuz
2001-02-23 cuz  24.396  24.440  24.127     24.036  73.451     NaN  73.733  71.136  71.418    35900.0  72.29 -0.03  cuz
2001-02-26 cuz  24.383  24.446  24.112     24.018  73.394     NaN  74.100  72.463  73.451    29100.0  72.55 -0.03  cuz
2001-02-27 cuz  24.374  24.451  24.100     23.972  73.253     NaN  73.677  72.124  73.394    25800.0  72.73 -0.03  cuz
2001-02-28 cuz  24.365  24.456  24.091     23.907  73.056     NaN  73.253  72.548  73.253    43600.0  72.86 -0.02  cuz
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22']
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           kmx      2.203     2.012     2.503      2.625     2.625     NaN     2.625     2.600     2.625    234400.0     2.58  0.20   kmx
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           pkoh     5.532     6.873     5.436      5.117     5.500     NaN     5.750     5.500     5.625      2200.0     5.45  0.21  pkoh
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           ghc    264.428   246.609   280.672    286.906   372.749     NaN   374.622   371.601   374.018     14500.0   371.18  0.03   ghc
           nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           fccy     2.962     2.988     3.519      3.805     3.961     NaN     3.961     3.961     3.961         0.0     3.95  0.31  fccy
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           hwbk     8.184     8.508     7.837      7.848    12.603     NaN    12.603    12.603    12.603       900.0    12.60  0.00  hwbk
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'])
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           hwbk     8.184     8.508     7.837      7.848    12.603     NaN    12.603    12.603    12.603       900.0    12.60  0.00  hwbk
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           ghc    264.428   246.609   280.672    286.906   372.749     NaN   374.622   371.601   374.018     14500.0   371.18  0.03   ghc
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           kmx      2.203     2.012     2.503      2.625     2.625     NaN     2.625     2.600     2.625    234400.0     2.58  0.20   kmx
           pkoh     5.532     6.873     5.436      5.117     5.500     NaN     5.750     5.500     5.625      2200.0     5.45  0.21  pkoh
           fccy     2.962     2.988     3.519      3.805     3.961     NaN     3.961     3.961     3.961         0.0     3.95  0.31  fccy
           bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=True)
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           hwbk     8.184     8.508     7.837      7.848    12.603     NaN    12.603    12.603    12.603       900.0    12.60  0.00  hwbk
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           ghc    264.428   246.609   280.672    286.906   372.749     NaN   374.622   371.601   374.018     14500.0   371.18  0.03   ghc
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           kmx      2.203     2.012     2.503      2.625     2.625     NaN     2.625     2.600     2.625    234400.0     2.58  0.20   kmx
           pkoh     5.532     6.873     5.436      5.117     5.500     NaN     5.750     5.500     5.625      2200.0     5.45  0.21  pkoh
           fccy     2.962     2.988     3.519      3.805     3.961     NaN     3.961     3.961     3.961         0.0     3.95  0.31  fccy
           bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
           fccy     2.962     2.988     3.519      3.805     3.961     NaN     3.961     3.961     3.961         0.0     3.95  0.31  fccy
           pkoh     5.532     6.873     5.436      5.117     5.500     NaN     5.750     5.500     5.625      2200.0     5.45  0.21  pkoh
           kmx      2.203     2.012     2.503      2.625     2.625     NaN     2.625     2.600     2.625    234400.0     2.58  0.20   kmx
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           ghc    264.428   246.609   280.672    286.906   372.749     NaN   374.622   371.601   374.018     14500.0   371.18  0.03   ghc
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           hwbk     8.184     8.508     7.837      7.848    12.603     NaN    12.603    12.603    12.603       900.0    12.60  0.00  hwbk
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[:5]
                 100ma  200ma   30ma  Adj Close  Close  Date.1   High    Low   Open    Volume   nma   pct  sk.1
Date       sk
2001-02-22 bios  1.478  1.786  1.598      1.688  1.688     NaN  1.875  1.625  1.875   22300.0  1.88  0.54  bios
           fccy  2.962  2.988  3.519      3.805  3.961     NaN  3.961  3.961  3.961       0.0  3.95  0.31  fccy
           pkoh  5.532  6.873  5.436      5.117  5.500     NaN  5.750  5.500  5.625    2200.0  5.45  0.21  pkoh
           kmx   2.203  2.012  2.503      2.625  2.625     NaN  2.625  2.600  2.625  234400.0  2.58  0.20   kmx
           trns  1.622  2.005  1.608      1.625  1.625     NaN  1.688  1.531  1.531    8600.0  1.73  0.18  trns
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[:10]
                 100ma  200ma   30ma  Adj Close  Close  Date.1   High    Low   Open    Volume   nma   pct  sk.1
Date       sk
2001-02-22 bios  1.478  1.786  1.598      1.688  1.688     NaN  1.875  1.625  1.875   22300.0  1.88  0.54  bios
           fccy  2.962  2.988  3.519      3.805  3.961     NaN  3.961  3.961  3.961       0.0  3.95  0.31  fccy
           pkoh  5.532  6.873  5.436      5.117  5.500     NaN  5.750  5.500  5.625    2200.0  5.45  0.21  pkoh
           kmx   2.203  2.012  2.503      2.625  2.625     NaN  2.625  2.600  2.625  234400.0  2.58  0.20   kmx
           trns  1.622  2.005  1.608      1.625  1.625     NaN  1.688  1.531  1.531    8600.0  1.73  0.18  trns
           ubp   2.402  2.331  2.578      2.772  8.050     NaN  8.100  8.000  8.000    7100.0  8.11  0.16   ubp
           res   0.991  0.906  1.039      1.024  1.745     NaN  1.771  1.732  1.771   17100.0  1.80  0.16   res
           pcyo  0.942  1.005  1.073      1.150  1.150     NaN  1.200  1.150  1.200    1500.0  1.19  0.15  pcyo
           anh   0.505  0.504  0.550      0.562  4.750     NaN  4.800  4.750  4.800    4600.0  4.87  0.15   anh
           ssys  1.212  1.708  1.055      1.000  1.000     NaN  1.052  0.958  1.010   84000.0  1.01  0.12  ssys
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[:10][mth['High']>3]
__main__:1: UserWarning: Boolean Series key will be reindexed to match DataFrame index.
                 100ma  200ma   30ma  Adj Close  Close  Date.1   High    Low   Open  Volume   nma   pct  sk.1
Date       sk
2001-02-22 fccy  2.962  2.988  3.519      3.805  3.961     NaN  3.961  3.961  3.961     0.0  3.95  0.31  fccy
           pkoh  5.532  6.873  5.436      5.117  5.500     NaN  5.750  5.500  5.625  2200.0  5.45  0.21  pkoh
           ubp   2.402  2.331  2.578      2.772  8.050     NaN  8.100  8.000  8.000  7100.0  8.11  0.16   ubp
           anh   0.505  0.504  0.550      0.562  4.750     NaN  4.800  4.750  4.800  4600.0  4.87  0.15   anh
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[:10][mth['Close']<mth['nma']]
                 100ma  200ma   30ma  Adj Close  Close  Date.1   High    Low   Open   Volume   nma   pct  sk.1
Date       sk
2001-02-22 bios  1.478  1.786  1.598      1.688  1.688     NaN  1.875  1.625  1.875  22300.0  1.88  0.54  bios
           trns  1.622  2.005  1.608      1.625  1.625     NaN  1.688  1.531  1.531   8600.0  1.73  0.18  trns
           ubp   2.402  2.331  2.578      2.772  8.050     NaN  8.100  8.000  8.000   7100.0  8.11  0.16   ubp
           res   0.991  0.906  1.039      1.024  1.745     NaN  1.771  1.732  1.771  17100.0  1.80  0.16   res
           pcyo  0.942  1.005  1.073      1.150  1.150     NaN  1.200  1.150  1.200   1500.0  1.19  0.15  pcyo
           anh   0.505  0.504  0.550      0.562  4.750     NaN  4.800  4.750  4.800   4600.0  4.87  0.15   anh
           ssys  1.212  1.708  1.055      1.000  1.000     NaN  1.052  0.958  1.010  84000.0  1.01  0.12  ssys
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[mth['Close']<mth['nma']]
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
>>> mth.iloc[mth.index.get_level_values('Date') == '2001-02-22'].sort_values(by=['pct'], ascending=False)[mth['Close']<mth['nma']]
                    100ma     200ma      30ma  Adj Close     Close  Date.1      High       Low      Open      Volume      nma   pct  sk.1
Date       sk
2001-02-22 bios     1.478     1.786     1.598      1.688     1.688     NaN     1.875     1.625     1.875     22300.0     1.88  0.54  bios
           trns     1.622     2.005     1.608      1.625     1.625     NaN     1.688     1.531     1.531      8600.0     1.73  0.18  trns
           ubp      2.402     2.331     2.578      2.772     8.050     NaN     8.100     8.000     8.000      7100.0     8.11  0.16   ubp
           res      0.991     0.906     1.039      1.024     1.745     NaN     1.771     1.732     1.771     17100.0     1.80  0.16   res
           pcyo     0.942     1.005     1.073      1.150     1.150     NaN     1.200     1.150     1.200      1500.0     1.19  0.15  pcyo
           anh      0.505     0.504     0.550      0.562     4.750     NaN     4.800     4.750     4.800      4600.0     4.87  0.15   anh
           ssys     1.212     1.708     1.055      1.000     1.000     NaN     1.052     0.958     1.010     84000.0     1.01  0.12  ssys
           anik     1.244     1.946     1.360      1.125     1.125     NaN     1.312     1.125     1.188      6000.0     1.29  0.12  anik
           scco     0.862     0.832     0.894      0.959     2.473     NaN     2.490     2.445     2.490     41400.0     2.48  0.11  scco
           hurc     3.332     3.610     3.362      3.498     3.750     NaN     4.188     3.438     4.188     10000.0     3.88  0.07  hurc
           bpt      1.442     1.288     1.563      1.637    14.200     NaN    14.690    14.070    14.490    161800.0    14.44  0.05   bpt
           ug       1.891     1.901     2.149      2.128     5.130     NaN     5.130     5.130     5.130      1000.0     5.27  0.05    ug
           alg     11.078    10.744    11.937     12.071    14.650     NaN    14.650    14.520    14.600      1100.0    14.83  0.05   alg
           dswl     2.212     2.106     2.320      2.235     7.222     NaN     7.444     7.222     7.222     11700.0     7.53  0.05  dswl
           mu      37.274    57.023    41.874     38.000    38.000     NaN    39.450    36.500    38.280   8415200.0    40.43  0.03    mu
           mro      5.204     5.066     5.261      5.325     8.327     NaN     8.440     8.303     8.411   3837700.0     8.40  0.01   mro
           stc     13.604    12.108    15.698     15.434    19.750     NaN    19.750    19.700    19.750     22400.0    20.23  0.00   stc
           ewh      6.788     7.074     7.060      6.914    11.750     NaN    11.820    11.590    11.750     38900.0    11.82 -0.02   ewh
           asys     9.272     8.744     9.811      7.125     7.125     NaN     7.406     6.500     7.219    121500.0     8.01 -0.02  asys
           myn      4.350     4.153     4.688      4.585    13.220     NaN    13.300    13.200    13.300     35300.0    13.39 -0.03   myn
           mays     8.917     7.900     9.721     10.125    10.125     NaN    10.250    10.125    10.250     14600.0    10.13 -0.04  mays
           aim   3063.086  3332.353  2582.888   2296.800  2296.800     NaN  2376.000  2270.400  2376.000         0.0  2353.82 -0.05   aim
           wmt     35.191    36.649    37.233     34.828    49.700     NaN    51.000    48.950    51.000   9154300.0    51.53 -0.06   wmt
           phi      6.614     6.627     7.020      6.577    16.900     NaN    17.100    16.810    16.880     97800.0    17.27 -0.06   phi
           cuz     24.414    24.435    24.140     23.288    71.164     NaN    72.406    70.628    72.406     65000.0    71.97 -0.06   cuz
           nke      4.629     4.386     5.322      4.742     6.004     NaN     6.048     5.671     5.890  18472800.0     6.16 -0.19   nke
>>>