-- CreateEnum
CREATE TYPE "VideoStatus" AS ENUM ('PROCESSING', 'CREATED', 'FAILED');

-- AlterTable
ALTER TABLE "Video" ADD COLUMN     "isPublic" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "status" "VideoStatus" NOT NULL DEFAULT 'PROCESSING';
