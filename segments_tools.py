import random

def validate_segments(segment=[58, 73, 79, 89],min_dif=5):
    for i in xrange(1,len(segment)):
        if segment[i] <= segment[i-1] + min_dif:
            return False
    return True

def get_segments_list_sample(length=100,n_segments=4,min_segment_size=5,num_samples=3):
    """
    Please refactor me, I'm ugly
    """
    segments_list = []
    for num_sample in xrange(num_samples):
        segments = [0]*n_segments
        segments[0] = random.randint(min_segment_size-1,length-n_segments*min_segment_size)
        good_segment = True
        for i in xrange(1,n_segments):
            try:
                a = segments[i-1]+min_segment_size
                b = length-min_segment_size*(n_segments-i+1)
                if a>=b: good_segment=False
                segments[i] = random.randint(a,b)
            except:
                good_segment=False
                break
        if good_segment:
            segments_list.append(segments)
    return segments_list


def segment_generator(length=300,num_segments=(3,20),min_segment_size=7):
    while True:
        segments = random.randint(num_segments[0],num_segments[1])
        a = get_segments_list_sample(length=length,n_segments=segments)
        if a==[]:
            continue
        yield a[0]

if __name__ == '__main__':
    iter = segment_generator()
    for i in xrange(20):
        print iter.next()
