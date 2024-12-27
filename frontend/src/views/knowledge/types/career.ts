export interface CareerPathStage {
  id: string
  name: string
  description: string
  difficulty: string
  tags: string[]
  keyPoints: string[]
  estimatedTime?: string
  prerequisites?: string[]
  resources?: {
    type: string
    items: {
      name: string
      url: string
      description: string
    }[]
  }[]
}

export interface CareerPathResponse {
  path: CareerPathStage[]
  estimatedTime: string
  difficulty: string
  prerequisites: string[]
}

export interface CareerPathRequest {
  career: string
  preferences?: {
    focusAreas?: string[]
    timeConstraint?: string
    currentLevel?: string
  }
} 