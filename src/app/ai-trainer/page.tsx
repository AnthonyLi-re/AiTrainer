import React, { useEffect, useRef } from 'react';
import * as posedetection from '@tensorflow-models/pose-detection';
import '@tensorflow/tfjs-backend-webgl';
import { Box, Typography, Card, CardContent } from '@mui/material';

const AiTrainer = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

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
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            AI Trainer
          </Typography>
          <Typography variant="body1" gutterBottom>
            Use this tool to track your exercises with real-time feedback.
          </Typography>
        </CardContent>
      </Card>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 3 }}>
        <video
          ref={videoRef}
          style={{
            width: '640px',
            height: '480px',
            border: '1px solid black',
            borderRadius: '8px',
          }}
        />
        <canvas
          ref={canvasRef}
          width="640"
          height="480"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
          }}
        />
      </Box>
    </Box>
  );
};

export default AiTrainer;
