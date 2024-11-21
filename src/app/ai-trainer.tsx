import React, { useRef, useEffect, useState } from 'react';
import * as posedetection from '@tensorflow-models/pose-detection';
import '@tensorflow/tfjs-backend-webgl';

const AiTrainer = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [reps, setReps] = useState(0);

  useEffect(() => {
    const setupCamera = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    };

    const loadModel = async () => {
      const detector = await posedetection.createDetector(
        posedetection.SupportedModels.BlazePose,
        { runtime: 'tfjs' }
      );

      const detectPose = async () => {
        if (videoRef.current && detector) {
          const poses = await detector.estimatePoses(videoRef.current);
          drawPose(poses);
        }
        requestAnimationFrame(detectPose);
      };

      detectPose();
    };

    const drawPose = (poses: posedetection.Pose[]) => {
      const ctx = canvasRef.current?.getContext('2d');
      if (ctx && poses.length > 0) {
        ctx.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);

        const keypoints = poses[0].keypoints;
        keypoints.forEach((kp) => {
          if (kp.score > 0.5) {
            ctx.beginPath();
            ctx.arc(kp.x, kp.y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'red';
            ctx.fill();
          }
        });
      }
    };

    setupCamera();
    loadModel();
  }, []);

  return (
    <div>
      <h1>AI Trainer</h1>
      <video ref={videoRef} style={{ width: '640px', height: '480px' }} />
      <canvas ref={canvasRef} width="640" height="480" />
    </div>
  );
};

export default AiTrainer;
