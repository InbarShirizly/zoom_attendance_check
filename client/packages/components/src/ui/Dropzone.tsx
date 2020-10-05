import React, { useState } from 'react'

interface DropzoneProps {
  children: React.ReactNode
  onDrop(files: File[]): void
}

const notNullGuard = <T extends {}>(f: T | null): f is T => f !== null

const itemsHaveFiles = (items: DataTransferItem[]) => items.some(item => item.kind === 'file')
const filesFromItems = (items: DataTransferItem[]) => items.map(item => item.getAsFile()).filter(notNullGuard)
const overrideEventDefaults = (event: React.DragEvent<HTMLDivElement>) => {
  event.preventDefault()
  event.stopPropagation()
}

/**
 * This defines a zone in the page as a "drop zone", where you can drop files and do whatever with them.
 * Optimized, hook based version of this: https://spin.atomicobject.com/2018/09/13/file-uploader-react-typescript/
 */
export const withDropzone = () => ({ children, onDrop }: DropzoneProps) => {
    const [isDragActive, setIsDragActive] = useState(false)
    let dragEventCounter = 0

    const dragEnterHandler = (event: React.DragEvent<HTMLDivElement>) => {
      overrideEventDefaults(event)

      dragEventCounter++

      const items = Array.from(event.dataTransfer.items)
      return itemsHaveFiles(items) && setIsDragActive(true)
    }

    const dragLeaveHandler = (event: React.DragEvent<HTMLDivElement>) => {
      overrideEventDefaults(event)

      dragEventCounter--

      return dragEventCounter === 0 && setIsDragActive(false)
    }

    const dropHandler = (event: React.DragEvent<HTMLDivElement>) => {
      overrideEventDefaults(event)

      dragEventCounter = 0

      const items = Array.from(event.dataTransfer.items)
      if (itemsHaveFiles(items)) {
        const files = filesFromItems(items)

        setIsDragActive(false)
        return onDrop(files)
      }
    }

    return (
      <div
        onDrop={dropHandler}
        onDragEnter={dragEnterHandler}
        onDragLeave={dragLeaveHandler}
        onDragOver={overrideEventDefaults}
      >
        {children}
      </div>
    )
  }
}
