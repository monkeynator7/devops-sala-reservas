@Library('sonarlibrary') _

pipeline {
  agent any

  triggers {
    gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'NameBasedFilter', includeBranchesSpec: 'feature/*', excludeBranchesSpec: '')
  }

  environment {
    ENVIRONMENT = "dev"
    DEPLOYMENT_FILE = "deploy/k8s/deployment.yaml"
    CONFIG_FILE = "deploy/k8s/configMap.yaml"
    SECRET_FILE = "deploy/k8s/secret.yaml"
    SERVICE_FILE = "deploy/k8s/service.yaml"
    SONAR_FILE = "deploy/sonar-project.properties"
    DRY_RUN = "--dry-run"
    APP_NAME = "TransChileApp"
    REPO_NAME = "transchile-service"
    HARBOR_URL = 'harbor.transchile.cl'
    HARBOR_ENV = 'develop'
  }

  stages {
    stage('Checkout Code') {
      steps {
        script {
          echo "Obteniendo código desde rama: ${env.GIT_BRANCH}"
        }
      }
    }

    stage('Bootstrap Environment') {
      steps {
        script {
          if (env.GIT_BRANCH.contains("develop")) {
            ENVIRONMENT = "qa"
            HARBOR_ENV = "release"
          } else if (env.GIT_BRANCH.contains("master")) {
            ENVIRONMENT = "prod"
            HARBOR_ENV = "production"
          }
          echo "Entorno configurado como: ${ENVIRONMENT}"
        }
      }
    }

    stage('Code Analysis') {
      steps {
        script {
          echo "Ejecutando análisis de calidad con SonarQube"
          sonarscanner()
        }
      }
    }

    stage('Build Image') {
      steps {
        script {
          echo "Construyendo imagen Docker para ${APP_NAME}"
          docker.build("${HARBOR_URL}/${HARBOR_ENV}/${APP_NAME}:${env.BUILD_NUMBER}")
        }
      }
    }

    stage('Deploy to Staging') {
      when {
        expression { ENVIRONMENT == "qa" }
      }
      steps {
        script {
          echo "Desplegando a entorno de QA"
          sh """
          kubectl apply -f ${DEPLOYMENT_FILE} --namespace=${TBS_CLUSTER_NAMESPACE}
          kubectl apply -f ${CONFIG_FILE} --namespace=${TBS_CLUSTER_NAMESPACE}
          """
        }
      }
    }

    stage('Deploy to Production') {
      when {
        expression { ENVIRONMENT == "prod" }
      }
      steps {
        script {
          echo "Desplegando a entorno de Producción"
          sh """
          kubectl apply -f ${DEPLOYMENT_FILE} --namespace=${TBS_CLUSTER_NAMESPACE}
          kubectl apply -f ${CONFIG_FILE} --namespace=${TBS_CLUSTER_NAMESPACE}
          """
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline completado exitosamente"
    }
    failure {
      echo "Error en el pipeline. Revisar los logs."
    }
  }
}
