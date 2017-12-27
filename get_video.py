# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 09:51:20 2017

@author: Quantum Liu
"""
import re,requests
import argpase
def get_video(videopage):
    #从播放页抓取视频详情，返回一个图片来了包括不同质量的MP4文件地址的一个字典，时长(秒)，一个包含浏览数、赞/踩比率和数量以及所属分类的字典。可单独使用。
    #Crawling detail of the video, return a tuple which has a dict of MP4 file's address of different qualities, the duration(second),a dict contains number of views, the rate and number of votes Up/Down.
    
    headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    proxies={'https': 'https://127.0.0.1:1080','http': 'http://127.0.0.1:1080'}
    r_v=r'"quality":".*?","videoUrl":"(.*?)"}'
    r_cover=r'"image_url":"(.*?)",'
    r_title=r'data-video-title="(.*?)"'
    r_quality=r'quality":"(\d*?)","videoUrl":".*?"}'
    r_duration=r'"video_duration":"(\d.*?)"'
    r_view=r'<div class="views"><span class="count">(.*?)</span>'
    r_percent=r'<span class="percent">(.*?)</span>'
    r_up=r'<span class="votesUp">(.*?)</span>'
    r_down=r'<span class="votesDown">(.*?)</span>'
    r_cate=r'<a href="/video.*?" onclick="ga.*?;">(.*?)</a>'
    html_text=requests.get(videopage,headers=headers,proxies=proxies).text
    l_v=list(map(lambda x:x.replace('\\',''),re.findall(r_v,html_text)))
    l_q=re.findall(r_quality,html_text)
    adds={q:v.replace('\\','') for q,v in zip(l_q,l_v)}
    duration=int(re.findall(r_duration,html_text)[0])
    title=re.findall(r_title,html_text)[0]
    infos={'duration':duration,'cover':re.findall(r_cover,html_text)[0].replace('\\',''),'views':re.findall(r_view,html_text)[0],'percent':re.findall(r_percent,html_text)[0],'up':re.findall(r_up,html_text)[0],'down':re.findall(r_down,html_text)[0],'categories':re.findall(r_cate,html_text)}
    return (adds,title,infos)

def show_infos(adds,title,infos):
    text='Video title:{}\nDuration:{}\nAvailable qualities:{}\nCategories:{}'
    cats=','.join(infos['categories'])
    duration=infos['duration']
    qualities='\n'.join([str(q)+' : '+str(url) for q,url in adds.items()])
    text=text.format(title,duration,qualities,cats)
    print(text)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='Target URL')
    args = parser.parse_args()
    show_infos(*get_video(args.url))
