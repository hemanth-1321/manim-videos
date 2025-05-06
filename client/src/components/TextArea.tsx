"use client";

import { useState } from "react";
import { PlaceholdersAndVanishInput } from "./ui/placeholders-and-vanish-input";
import { BACKEND_URL } from "@/lib/config";
import axios from "axios";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
export function TextArea() {
  const [inputValue, setInputValue] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
 const router=useRouter()
  const placeholders = [
    "Animate a square rotating 360 degrees.",
    "Animate a ball bouncing up and down.",
    "Animate a sine wave oscillating horizontally.",
    "Animate a dot moving along a path",
    "Animate a 3D cube rotating along all axes",
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const pollStatus = async (jobId: string) => {
    const token = localStorage.getItem("token");
    let attempts = 0;
    const maxAttempts = 30; // e.g., 30 x 2s = 1 minute timeout

    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/status/${jobId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.data.status === "done") {
          clearInterval(interval);
          setIsProcessing(false);
          toast.success("Video created! Check 'My Videos'.");
        } else if (res.data.status === "error") {
          clearInterval(interval);
          setIsProcessing(false);
          toast.error("Failed to generate video.");
        }

        attempts++;
        if (attempts >= maxAttempts) {
          clearInterval(interval);
          setIsProcessing(false);
          toast.error("Video generation timed out.");
        }
      } catch (err) {
        clearInterval(interval);
        setIsProcessing(false);
        toast.error("Error while checking video status.");
      }
    }, 2000); // 2 seconds
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No token found");
      toast.error("Please log in first.");
      return;
    }

    try {
      setIsProcessing(true);
      toast.loading("Processing your video... Please wait!", { id: "processing", duration: Infinity });

      const response = await axios.post(
        `${BACKEND_URL}/submit`,
        { prompt: inputValue },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const jobId = response.data.jobId;
      if (!jobId) throw new Error("No jobId returned from backend");

      pollStatus(jobId);
      router.refresh()
    } catch (error: any) {
      setIsProcessing(false);
      toast.dismiss("processing"); 
      console.error("Submission failed:", error.response?.data || error.message);
      
    }
  };

  return (
    <div className="h-[40rem] flex flex-col justify-center items-center px-4">
      <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl dark:text-white text-black">
        Generate Video Animations
      </h2>
      <p className="text-center mb-6 text-muted-foreground text-sm max-w-xl">
        Enter a natural language prompt to generate math or physics animations using Manim.
        You'll receive a rendered video preview.
      </p>
      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={handleChange}
        onSubmit={onSubmit}
        ondisabled={isProcessing}
      />
    </div>
  );
}
