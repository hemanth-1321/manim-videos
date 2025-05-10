'use client';

import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '@/lib/config';
import { Download } from 'lucide-react';
import { useAuthStore } from '@/stores/useAuth';
import { toast } from 'sonner';

interface Video {
  id: string;
  url: string;
  username?: string;
  created_at: string;
}

interface RawVideo {
  id: string;
  url: string;
  created_at: string; 
  user?: {
    email: string;
  };
}

export default function VideoGallery() {
  const [allVideos, setAllVideos] = useState<Video[]>([]);
  const [userVideos, setUserVideos] = useState<Video[]>([]);

  const { token, setToken } = useAuthStore();

  const fetchAllVideos = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/video`);
      const rawVideos: RawVideo[] = response.data?.response || [];

      const formatted = rawVideos.map((v) => ({
        id: v.id,
        url: v.url,
        username: v.user?.email || 'anonymous',
        created_at: v.created_at || '',
      }));

      setAllVideos(formatted);
    } catch (error) {
      console.error('Error fetching all videos:', error);
    }
  };

  const fetchUserVideos = useCallback(async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/user/video`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const rawVideos: RawVideo[] = response.data?.response || [];

      const formatted = rawVideos.map((v) => ({
        id: v.id,
        url: v.url,
        created_at: v.created_at || '',
      }));

      setUserVideos(formatted);
    } catch (error) {
      console.error('Error fetching user videos:', error);
    }
  }, [token]);

  useEffect(() => {
    const storedToken = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (storedToken) setToken(storedToken);
    fetchAllVideos();
  }, [setToken]);

  useEffect(() => {
    if (!token){ 
      toast.warning("Please login")
      return
    }
    const interval = setInterval(() => {
      fetchUserVideos();

    }, 5000); 
    return () => clearInterval(interval); 

  }, [token, fetchUserVideos]);

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <Tabs defaultValue="all" className="w-full">
        <TabsList className="flex justify-center mb-6">
          <TabsTrigger value="all">All Videos</TabsTrigger>
          <TabsTrigger value="user">My Videos</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <VideoGrid videos={allVideos} />
        </TabsContent>

        <TabsContent value="user">
          {token ? (
            <VideoGrid videos={userVideos} />
          ) : (
            <p className="text-center font-bold">Login to view your videos.</p>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

function VideoGrid({ videos }: { videos: Video[] }) {
  const [showDownload, setShowDownload] = useState<string | null>(null);

  if (!videos.length) {
    return <p className="text-center text-gray-400">No videos found.</p>;
  }

  const handleDownload = (url: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = `video-${Date.now()}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleVideoClick = (videoId: string) => {
    setShowDownload((prev) => (prev === videoId ? null : videoId));
  };

  return (
    <div className="columns-1 sm:columns-2 md:columns-3 gap-4 space-y-4">
      {videos.map((video) => (
        <div
          key={video.id}
          className="relative group overflow-hidden rounded-xl shadow-md break-inside-avoid border border-gray-300"
        >
          <video
            src={video.url}
            className="w-full h-auto rounded-xl transition-all duration-300 group-hover:scale-105"
            loop
            muted
            playsInline
            onMouseOver={(e) => e.currentTarget.play()}
            onMouseOut={(e) => e.currentTarget.pause()}
            onClick={() => handleVideoClick(video.id)}
          />

          <button
            onClick={() => handleDownload(video.url)}
            className="absolute top-4 right-4 p-2 bg-opacity-50 rounded-full shadow-md md:hover:bg-opacity-80 transition opacity-0 group-hover:opacity-100"
          >
            <Download className="cursor-pointer text-white" size={24} />
          </button>

          {showDownload === video.id && (
            <button
              onClick={() => handleDownload(video.url)}
              className="absolute top-4 right-4 p-2 bg-opacity-50 rounded-full shadow-md opacity-100"
            >
              <Download className="cursor-pointer text-white" size={24} />
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
