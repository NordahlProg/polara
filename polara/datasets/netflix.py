import pandas as pd
import tarfile


def get_netflix_data(gz_file):
    movie_data = []
    movie_inds = []
    with tarfile.open(gz_file) as tar:
        training_data = tar.getmember('download/training_set.tar')
        with tarfile.open(fileobj=tar.extractfile(training_data)) as inner:
            for item in inner.getmembers():
                if item.isfile():
                    f = inner.extractfile(item.name)
                    df = pd.read_csv(f)
                    movieid = df.columns[0]
                    movie_inds.append(int(movieid[:-1]))
                    movie_data.append(df[movieid])

    data = pd.concat(movie_data, keys=movie_inds)
    data = data.reset_index().iloc[:, :3].rename(columns={'level_0': 'movieid',
                                                          'level_1': 'userid',
                                                          'level_2': 'rating'})
    return data
